# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################


from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, date, datetime
import calendar


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('draft', 'พิจารณาสินเชื่อ'),
        ('sent', 'แจ้งสถานะ'),
        ('sale', 'รอทำสัญญา'),
        ('invoiced', 'ทำสัญญาแล้ว'),
    ])
    invoice_status = fields.Selection(selection_add=[
        ('to invoice', 'รอทำสัญญา'),
        ('invoiced', 'ทำสัญญาแล้ว'),
        ('no', 'จ่ายเงินกู้แล้ว')
    ])

    def action_confirm(self):
        # เรียกใช้ฟังก์ชันเดิม
        res = super(SaleOrder, self).action_confirm()

        # Update ฟิลด์อื่น ๆ
        for line in self.order_line:
            product_template = line.product_id.product_tmpl_id
            if product_template and product_template.wht:
                line.sdwht = product_template.wht

        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        # เรียกใช้ฟังก์ชันเดิมในการสร้างใบแจ้งหนี้
        invoices = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)

        invoice_status = self.invoice_status
        print(invoice_status)
        # ปรับเปลี่ยน state ของ sale order เป็น "invoiced"
        self.write({'state': 'invoiced'})

        return invoices


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sdwht = fields.Boolean('ภาษีหัก ณ.ที่จ่าย')
    amtwht = fields.Float('ภาษีหักไว้')
    # ปอนด์ทำ
    interest = fields.Float(string='ดอกเบี้ย')
    principle = fields.Float(string='เงินต้น')
    # บี๊บ
    no_periods = fields.Integer(string='งวดที่', readonly=True)
    due_date_periods = fields.Date(string='วันที่ต้องจ่าย')
    overdue = fields.Selection([('1-30', '1-30'),
                                ('31-60', '31-60'),
                                ('61-90', '61-90'),
                                ('91-120', '91-120'),
                                ('121-150', '121-150'),
                                ('151-180', '151-180'),
                                ('180 ขึ้นไป', '180 ขึ้นไป')], required=True, default='1-30')
    total = fields.Float(string='ราคารวม')
    price_subtotal = fields.Monetary(compute='_compute_price_subtotal', store=True)


    @api.model
    def create(self, vals):
        # Check if the product_id is in the vals and fetch the related product
        if 'product_id' in vals:
            product = self.env['product.product'].browse(vals.get('product_id'))
            if product:
                product_template = product.product_tmpl_id
                # Set sdwht and amtwht based on the wht field in the product template
                vals['sdwht'] = product_template.wht
                vals['amtwht'] = vals['price_unit'] * vals['product_uom_qty'] * product_template.wht_per / 100
            else:
                vals['sdwht'] = False
                vals['amtwht'] = False
        else:
            # Default behavior if product_id is not provided
            vals['sdwht'] = False
            vals['amtwht'] = False

        # Call the super method to create the record
        return super(SaleOrderLine, self).create(vals)

    @api.depends('price_unit', 'interest')
    def _compute_price_subtotal(self):
        for line in self:
            # คำนวณ subtotal จาก `price_unit` และ `interest`
            line.price_subtotal = line.price_unit + (line.interest or 0)

        # คำนวณ `amount_untaxed` ใน `sale.order` เมื่อ `price_subtotal` ของ `sale.order.line` เปลี่ยนแปลง
        for line in self:
            # ให้แน่ใจว่าเราเข้าถึง `order_id` ของแต่ละ `line`
            order = line.order_id
            if order:
                total_untaxed = sum(line.price_subtotal for line in order.order_line)
                order.amount_untaxed = total_untaxed  # อัปเดตยอดรวมก่อนภาษีใน `sale.order

    # เมื่อบันทึกข้อมูลใหม่, คำนวณ subtotal ใหม่
    @api.model
    def create(self, vals):
        record = super(SaleOrderLine, self).create(vals)
        return record

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        return res


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        # สร้างใบแจ้งหนี้จากคำสั่งขาย
        invoices = self._create_invoices(self.sale_order_ids)

        seen_invoices = set()  # สร้าง set เพื่อเก็บ invoice.id ที่บันทึกไปแล้ว

        for order in self.sale_order_ids:
            for sale_line in order.order_line:
                # ค้นหา invoice ที่ถูกสร้างจากคำสั่งขาย
                for invoice in order.invoice_ids:
                    no_periods = sale_line.no_periods
                    i = 0  # เริ่มต้นตัวแปร i

                    # เช็คว่าเราเคยบันทึก invoice นี้ไปแล้วหรือยัง
                    if invoice.id not in seen_invoices:
                        # ค้นหาแถวแรกจาก account.move.line ของใบแจ้งหนี้นี้
                        first_invoice_line = self.env['account.move.line'].search([
                            ('move_id', '=', invoice.id)  # ค้นหาจาก move_id ของใบแจ้งหนี้
                        ], limit=1)  # จำกัดผลลัพธ์ให้เป็นแถวแรก

                        # ถ้าพบแถวแรกแล้ว
                        if first_invoice_line:
                            # บันทึกแค่แถวแรกลงใน new.account.move.line
                            self.env['new.account.move.line'].create({
                                'principle': first_invoice_line.price_unit,
                                'remaining_principal': invoice.amount_total,
                                'line_ids': invoice.id,  # Referring to the accounting move
                            })
                            # บันทึกว่าเราได้บันทึก invoice นี้ไปแล้ว
                            seen_invoices.add(invoice.id)

                    # คำนวณ due_date ตาม approve_date และ no_periods
                    due_date = self._get_end_of_month(order.approve_date, i)

                    # เช็คว่า product_id ของ sale_line ตรงกับ invoice_line หรือไม่
                    for invoice_line in invoice.invoice_line_ids:
                        if invoice_line.product_id == sale_line.product_id:
                            # คัดลอกค่า sdwht และ amtwht จาก sale order line ไปที่ invoice line
                            invoice_line.asdwht = sale_line.sdwht
                            invoice_line.asdamtwht = sale_line.amtwht
                            # กำหนด no_periods ให้ตรงกับ sale_line
                            invoice_line.no_periods = i + 1
                            invoice_line.due_date_periods = due_date
                            invoice_line.overdue = sale_line.overdue
                            i += 1  # เพิ่มค่า i ทีละ

        # ส่ง invoice ที่เปิดถ้ามี
        if self.env.context.get('open_invoices'):
            return self.sale_order_ids.action_view_invoice()

        return {'type': 'ir.actions.act_window_close'}

    def _get_end_of_month(self, date, months_offset):
        """ คำนวณวันสุดท้ายของเดือนจากวันที่ระบุและจำนวนเดือนที่เพิ่ม """
        year = date.year
        month = date.month + months_offset

        if month > 12:
            month -= 12
            year += 1
        elif month < 1:
            month += 12
            year -= 1

        # ใช้ calendar.monthrange เพื่อหาจำนวนวันในเดือนนั้น
        last_day = calendar.monthrange(year, month)[1]

        return date.replace(year=year, month=month, day=last_day)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    asdwht = fields.Boolean(string='ภาษีหัก ณ.ที่จ่าย')
    asdamtwht = fields.Float(string='ภาษีหักไว้')

    @api.model
    def create(self, vals):
        move_id = self.move_id
        acc_id = self.account_id
        print(acc_id)
        print(move_id)
        # เพิ่มค่าของ sdwht และ amtwht ถ้ามีใน context
        if self.env.context.get('from_sale_order'):
            sale_line = self.env['sale.order.line'].browse(self.env.context['sale_order_line_id'])
            vals['asdwht'] = sale_line.sdwht
            vals['asdamtwht'] = sale_line.amtwht

        return super(AccountMoveLine, self).create(vals)


class ProductTemplateMaster(models.Model):
    _inherit = "product.template"

    wht = fields.Boolean('ภาษีหัก ณ.ที่จ่าย')
    wht_per = fields.Integer('ภาษีหัก ณ.ที่จ่าย%')
    adv = fields.Boolean('หักเงินล่วงหน้า')
    adv_per = fields.Integer('หักเงินล่วงหน้าที่จ่าย%')


# ของบี๊บทำ
class SaleOrderEdit(models.Model):
    _inherit = "sale.order"

    number = fields.Char(string='ลำดับสัญญา')
    branch = fields.Many2one('branch', string='สาขา')
    contract_number = fields.Char(string='เลขที่สัญญา')
    cus_number = fields.Char(string='รหัสลูกค้า')
    date_contract = fields.Date(string='วันที่ทำสัญญา')
    credit_limit = fields.Float(string='วงเงินสินเชื่อ')
    remaining_principal = fields.Float(string='เงินต้นคงเหลือ')
    accrued_interest = fields.Float(string='ดอกเบี้ยค้างรับ')
    fine = fields.Float(string='ค่าปรับ (ถ้ามี)')
    tracking_fee = fields.Float(string='ค่าติดตาม (ถ้ามี)')
    overdue_installment = fields.Float(string='ค้างงวด')
    installment = fields.Float(string='ค่างวดๆละ')
    latest_payment = fields.Float(string='ชำระล่าสุด')
    owed_a_fine = fields.Float(string='ค่าเบี้ยปรับ')
    bill_coll = fields.Char(string='Bill coll')
    registration = fields.Char(string='เลขทะเบียน (ถ้ามี)')
    chassis_number = fields.Char(string='เลขตัวถัง (ถ้ามี)')
    address = fields.Char(string='ที่อยู่')
    all_periods = fields.Integer(string='งวดทั้งหมด')
    outstanding_installment = fields.Char(string='งวดที่ค้าง')
    from_the_period = fields.Char(string='จากงวดที่')
    car_model = fields.Char(string='รุ่นรถ (ถ้ามี)')
    car_color = fields.Char(string='สีรถ (ถ้ามี)')
    guarantor_code1 = fields.Char(string='รหัสผู้ค้ำ 1 (ถ้ามี)')
    guarantor_code2 = fields.Char(string='รหัสผู้ค้ำ 2 (ถ้ามี)')
    name_guarantor1 = fields.Char(string='ชื่อ-นามสกุลผู้ค้ำ 1 (ถ้ามี)')
    name_guarantor2 = fields.Char(string='ชื่อ-นามสกุลผู้ค้ำ 2 (ถ้ามี)')
    address_guarantor1 = fields.Char(string='ที่อยู่ผู้ค้ำ 1 (ถ้ามี)')
    address_guarantor2 = fields.Char(string='ที่อยู่ผู้ค้ำ 2 (ถ้ามี)')
    latest_payment_amount = fields.Float(string='จำนวนเงินที่ชำระล่าสุด')
    number_of_days_missed = fields.Float(string='จำนวนวันขาดงวด')
    dew_day = fields.Date(string='วันดิวเริ่มขาดงวด')

    product = fields.Many2one('product.product', string='ของค้ำประกัน')
    amount = fields.Float(string='จำนวนเงินที่กู้')

    approve_date = fields.Date(string='วันที่ยืนยัน')

    def action_confirm(self):
        super(SaleOrderEdit, self).action_confirm()

        # สร้าง line ใน sale.order.line ตามจำนวนใน all_periods
        for order in self:
            if order.approve_date is None:
                raise ValidationError("คุณยังไม่ได้ใส่วันที่ยืนยัน กรุณาใส่วันที่ยืนยันก่อนดำเนินการต่อ")

            if order.all_periods > 0:
                amount = order.amount / order.all_periods  # ใช้ amount ของ order แทน self.amount
                order.approve_date = fields.Datetime.now()

                for i in range(order.all_periods):  # สำหรับจำนวนรอบที่กำหนดใน all_periods
                    due_date = self._get_end_of_month(order.approve_date, i)

                    # คำนวณดอกเบี้ยจาก amount ของ order
                    interest = (amount * 0.5) / 100  # คำนวณดอกเบี้ยจาก amount และ 0.5%

                    # คำนวณราคา
                    total = amount + interest  # รวม amount และ interest เพื่อคำนวณราคาสุทธิ

                    # หาผลรวมของ price_subtotal จากทุกบรรทัดใน sale.order.line ที่เกี่ยวข้อง
                    total_subtotal = sum(line.price_subtotal for line in order.order_line)

                    # อัปเดตฟิลด์ amount_untaxed และ amount_total
                    order.amount_untaxed = total_subtotal
                    order.amount_total = total_subtotal + order.amount_tax

                    # สร้าง sale order line ใหม่
                    self.env['sale.order.line'].create({
                        'order_id': order.id,
                        'product_id': order.product.id,
                        'product_uom_qty': 1,  # ปริมาณที่ต้องการ
                        'price_unit': amount,  # ราคาต่อหน่วย (จาก amount ที่คำนวณ)
                        'no_periods': i + 1,
                        'due_date_periods': due_date,
                        'interest': interest,
                        # 'total': total,  # รวมราคาพร้อมดอกเบี้ย
                        # 'price_subtotal': total
                    })

    def _get_end_of_month(self, date, months_offset):
        """ คำนวณวันสุดท้ายของเดือนจากวันที่ระบุและจำนวนเดือนที่เพิ่ม """
        year = date.year
        month = date.month + months_offset

        if month > 12:
            month -= 12
            year += 1
        elif month < 1:
            month += 12
            year -= 1

        # ใช้ calendar.monthrange เพื่อหาจำนวนวันในเดือนนั้น
        last_day = calendar.monthrange(year, month)[1]

        return date.replace(year=year, month=month, day=last_day)



class AccountMoveLineEdit(models.Model):
    _inherit = 'account.move.line'

    no_periods = fields.Integer(string='งวดที่', readonly=True)
    paid_date_periods = fields.Date(string='วันที่จ่าย', readonly=True)
    due_date_periods = fields.Date(string='วันที่ต้องจ่าย')
    overdue = fields.Selection([('1-30', '1-30'),
                                ('31-60', '31-60'),
                                ('61-90', '61-90'),
                                ('91-120', '91-120'),
                                ('121-150', '121-150'),
                                ('151-180', '151-180'),
                                ('180 ขึ้นไป', '180 ขึ้นไป')], required=True, default='1-30')
    principle = fields.Float(string='เงินต้น')
    interest = fields.Float(string='ดอกเบี้ย')
    fine = fields.Float(string='ค่าปรับ')
    tracking_fee = fields.Float(string='ค่าติดตาม')
    outstanding_balance = fields.Float(string='ยอดค้างชำระ')
    total_collected = fields.Float(string='รวมต้องเก็บ')
    remaining_principal = fields.Float(string='เงินต้นคงเหลือ')
    # ปอนด์ทำ
    payment_pay = fields.Boolean(string='จ่ายแล้ว', readonly=True)
    overdue_alert = fields.Html(compute='_compute_overdue_alert', string="Overdue Alert")
    out_balance = fields.Float(string='ยอดค้างชำระ')
    pay_datetime = fields.Datetime(string='เวลาปัจจุบัน', default=fields.Datetime.now)
    paid_balance = fields.Float(string='ยอดที่ทำการชำระ')


    @api.model
    def your_button_action(self):
        # Add your logic here
        return True




    @api.depends('due_date_periods', 'overdue')
    def _compute_due_date_periods(self):
        for line in self:
            if line.overdue and line.due_date_periods:
                # ตรวจสอบว่า Overdue เป็น "1-30" หรือไม่
                days_to_add = 30 if line.overdue == "1-30" else 0
                line.due_date_periods = line.due_date_periods + timedelta(days=days_to_add)
            else:
                line.due_date_periods = line.due_date_periods

    @api.depends('due_date_periods')
    def _compute_overdue_alert(self):
        for line in self:
            # ถ้าวันที่ปัจจุบันเกิน due_date_periods แล้ว ให้แสดงแจ้งเตือนสีแดง
            if line.due_date_periods and date.today() > line.due_date_periods:
                line.overdue_alert = '<span style="color: red;">เกินกำหนดชำระ</span>'
            else:
                line.overdue_alert = ""
    # ทำใหม่


# ปอนด์ทำ
class PaymentEdit(models.TransientModel):
    _inherit = 'account.payment.register'

    pay_period = fields.Integer(string='งวดที่จ่าย', required=True)
    money = fields.Float(string='ยอดคงเหลือ')

    # inherit ปุ่มสร้างการชำระเงิน
    def action_create_payments(self):
        for record in self:
            invoices = self.env['account.move'].search([('name', '=', record.communication)])
            for invoice in invoices:
                all_paid = True  # ตัวแปรเพื่อเช็คว่าจ่ายครบหรือไม่
                for line in invoice.invoice_line_ids:
                    if line.no_periods == record.pay_period:
                        line.payment_pay = True
                        line.paid_date_periods = record.payment_date

                    # เช็คว่า payment_pay ทุกบรรทัดเป็น True หรือไม่
                    if not line.payment_pay:
                        all_paid = False

                # เปลี่ยนสถานะของ invoice ตามเงื่อนไข
                if all_paid:
                    invoice.payment_state = 'paid'  # เปลี่ยนสถานะเป็น paid
                else:
                    invoice.payment_state = 'partial'  # เปลี่ยนสถานะเป็น partial
                amount_residual = invoices.amount_residual - self.amount
                invoices.amount_residual = amount_residual

                # ลบข้อมูลที่เกี่ยวข้องใน new.account.move.line
                # ตัวอย่างนี้ลบข้อมูลทั้งหมดที่เชื่อมโยงกับ invoice ปัจจุบัน
                records_to_delete = self.env['new.account.move.line'].search([('line_ids', '=', invoice.id)])
                records_to_delete.unlink()

                # สร้าง record ใหม่ใน new.account.move.line
                self.env['new.account.move.line'].create({
                    'principle': line.price_subtotal,  # ตัวอย่างการกำหนดค่าจากฟิลด์ที่ต้องการ
                    'remaining_principal': invoice.amount_residual,
                    'line_ids': invoice.id,  # เชื่อมโยงกับ account.move (invoice)
                    # 'move_id': invoice.id,  # เชื่อมโยงกับ invoice
                    # เพิ่มฟิลด์อื่นๆ ตามที่ต้องการ
                })

                counter = 0

                self.env['new.account.move.line2'].create({
                    'id': counter,
                    'principle': line.price_subtotal,  # ตัวอย่างการกำหนดค่าจากฟิลด์ที่ต้องการ
                    'remaining_principal': invoice.amount_residual,
                    'line_ids': invoice.id,  # เชื่อมโยงกับ account.move (invoice)
                    # 'move_id': invoice.id,  # เชื่อมโยงกับ invoice
                    # เพิ่มฟิลด์อื่นๆ ตามที่ต้องการ
                })

                # เพิ่ม counter ทีละ 1
                counter += 1

                amount = self.amount  # หรืออาจจะได้จากฟิลด์ของ record เช่น `record.amount`
                # คำนวณเปอร์เซ็นต์จาก price_subtotal ของ invoice
                if line.price_subtotal and amount:
                    percentage = (amount / line.price_subtotal) * 100
                else:
                    percentage = 0.0  # ถ้าไม่มีค่า invoice.price_subtotal หรือ amount กำหนดเปอร์เซ็นต์เป็น 0

                amount2 = line.price_subtotal
                if line.price_subtotal and amount2:
                    percentage2 = (amount2 / self.amount) * 100
                else:
                    percentage2 = 0.0

                # สร้าง record ใหม่ใน new.account.move.line3
                self.env['new.account.move.line3'].create({
                    'price_collected': percentage2,
                    'principle': percentage,  # กำหนดค่าจากฟิลด์ที่ต้องการ
                    'line_ids': invoice.id,  # เชื่อมโยงกับ account.move (invoice)
                    # เพิ่มฟิลด์อื่นๆ ตามที่ต้องการ
                })

    @api.onchange('amount')
    def change_money(self):
        invoices = self.env['account.move'].search([('name', '=', self.communication)])
        self.money = invoices.amount_residual - self.amount


class AccountMoveEdit(models.Model):
    _inherit = 'account.move'

    employee_id = fields.Many2one('hr.employee', string='พนักงานเก็บเงิน')
    new_line = fields.One2many('new.account.move.line', 'line_ids', copy=True, readonly=True)
    new_line2 = fields.One2many('new.account.move.line2', 'line_ids', copy=True, readonly=True)
    new_line3 = fields.One2many('new.account.move.line3', 'line_ids', copy=True, readonly=True)

    receipt_contract = fields.Many2one('contract.details', string='เลขที่สัญญา')
    receipt_contract_code = fields.Char(string='รหัสสัญญา')

    paid_date_last = fields.Datetime(string='วันที่จ่ายล่าสุด')
    paid_date = fields.Char(string='จ่ายทุกวันที่')
    period_last = fields.Char(string='งวดที่จ่ายล่าสุด')

    @api.onchange('receipt_contract')
    def onchage(self):
        self.receipt_contract_code = self.receipt_contract.contract_code


    def _compute_name(self):
        for record in self:
            record.receipt_contract = record.receipt_contract.contract_code


class AccountMoveLineEdit(models.Model):
    _name = 'new.account.move.line'

    principle = fields.Float(string='เงินต้น')
    interest = fields.Float(string='ดอกเบี้ย/ค่าธรรมเนียม')
    fine = fields.Float(string='ค่าปรับ')
    tracking_fee = fields.Float(string='ค่าติดตาม')
    outstanding_balance = fields.Float(string='ยอดค้างชำระ')
    total_collected = fields.Float(string='รวมต้องเก็บ')
    remaining_principal = fields.Float(string='เงินต้นคงเหลือ')
    line_ids = fields.Many2one('account.move')


class AccountMoveLineEdit2(models.Model):
    _name = 'new.account.move.line2'

    period = fields.Integer(string='งวดที่')
    date_paid = fields.Datetime(string='วันที่จ่าย')
    principle = fields.Float(string='จำนวนที่จ่าย')
    interest = fields.Float(string='ดอกเบี้ย/ค่าธรรมเนียม')
    fine = fields.Float(string='ค่าปรับ')
    tracking_fee = fields.Float(string='ค่าติดตาม')
    outstanding_balance = fields.Float(string='คงเหลือต้องจ่าย')
    total_collected = fields.Float(string='รวมต้องเก็บ')
    remaining_principal = fields.Float(string='เงินต้นคงเหลือ')
    line_ids = fields.Many2one('account.move')


class AccountMoveLineEdit3(models.Model):
    _name = 'new.account.move.line3'

    price_collected = fields.Float(string='% จำนวนเงินที่เก็บได้')
    principle = fields.Float(string='% เงินต้น')
    interest = fields.Float(string='% ดอกเบี้ย/ค่าธรรมเนียม')
    fine = fields.Float(string='% ค่าปรับ')
    tracking_fee = fields.Float(string='% ค่าติดตาม')
    remaining_principal = fields.Float(string='% เงินต้นคงเหลือ')
    line_ids = fields.Many2one('account.move')


class PrintReport(models.Model):
    _name = 'print.report'

    date_from = fields.Date(string='ตั้งแต่วันที่วันที่')
    date_to = fields.Date(string='ถึงวันที่')

    def print_report(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "/web/binary/report_credit?date_from=%s&date_to=%s" % (self.date_from, self.date_to),
            "target": "new",
        }
