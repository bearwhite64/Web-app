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

from odoo import models, api, fields, _


class PaymentsReceiptHeaders(models.Model):
    _name = 'payments.receipt.headers'
    _description = 'ข้อมูลใบเสร็จรับเงิน'
    _rec_name = 'receipt_no'

    receipt_no = fields.Char(string='รหัสใบเสร็จ ')
    receipt_contract_id = fields.Many2one('contract.details', string='เลขที่สัญญา')
    receipt_contract_code = fields.Char(string='รหัสสัญญา')
    receipt_loan_type = fields.Char(string='ประเภทสินเชื่อ')
    receipt_product_code = fields.Char(string='รหัสสินค้า')
    receipt_service_code = fields.Char(string='รหัสบริการ')
    receipt_vat_rate = fields.Float(string='อัตราภาษีมูลค่าเพิ่ม')
    receipt_vat_amount = fields.Float(string='จำนวนภาษีมูลค่าเพิ่ม')
    receipt_tax_amount = fields.Float(string='จำนวนภาษี')
    receipt_amount = fields.Float(string='จำนวนเงิน')
    receipt_total_amount = fields.Float(string='ยอดเงิน')
    receipt_total_amount_text = fields.Char(string='ยอดเงินอักษร')
    receipt_reconcile_date = fields.Datetime(string='วันที่ Reconcile')
    receipt_date = fields.Datetime(string='วันที่ทำรายการ')
    receipt_cancel_by = fields.Char(string='ยกเลิกโดย')
    receipt_cancel_date = fields.Datetime(string='วันที่ยกเลิก')
    receipt_reason_code = fields.Char(string='รหัส Reason')
    receipt_reason_desc = fields.Char(string='คำอธิบายของ Reason')
    receipt_reference_date = fields.Datetime(string='วันที่ Reference')
    receipt_remark = fields.Char(string='หมายเหตุ')
    receipt_temp_no = fields.Char(string='รหัส Template')
    receipt_brand = fields.Char(string='แบรนด์')
    receipt_mailing_name = fields.Char(string='ชื่อผู้ติดต่อ')
    receipt_mailing_address = fields.Char(string='ที่อยู่ผู้ติดต่อ')
    receipt_engine_no = fields.Char(string='เลขเครื่อง')
    receipt_cust_name = fields.Char(string='ชื่อลูกค้า')
    receipt_cust_name1 = fields.Many2one('res.partner', string='ชื่อลูกค้า')
    receipt_cust_address = fields.Char(string='ที่อยู่ลูกค้า')
    receipt_print_date = fields.Datetime(string='วันที่พิมพ์ใบเสร็จ')
    receipt_status = fields.Char(string='สถานะรายการ')
    receipt_create_by = fields.Char(string='ผู้สร้างรายการ')
    receipt_create_date = fields.Datetime(string='วันที่สร้างรายการ')
    receipt_update_by = fields.Char(string='ผู้แก้ไขล่าสุด')
    receipt_update_date = fields.Datetime(string='วันที่แก้ไขล่าสุด')
    receipt_comp_code = fields.Char(string='รหัสบริษัทของผู้ทำรายการ')
    receipt_branch_code = fields.Char(string='รหัสสาขาของผู้ทำรายการ')
    receipt_receiver_fullname = fields.Char(string='ชื่อเต็มผู้รับ')
    receipt_customer_id = fields.Integer(string='รหัสลูกค้า')
    receipt_prin_bal_amt = fields.Float(string='จำนวนเงินต้นคงเหลือ')
    receipt_int_bal_amt = fields.Float(string='จำนวนดอกเบี้ยคงเหลือ')
    receipt_fee_bal_amt = fields.Float(string='จำนวนค่าธรรมเนียมคงเหลือ')
    receipt_dit_amt = fields.Float(string='ค่าขนส่ง')
    receipt_flag_settle = fields.Boolean(string='สถานะ การ Settle')
    receipt_write_off_flag = fields.Boolean(string='สถานะ การ WriteOff')
    receipt_stmd_id = fields.Integer(string='รหัส Statement Detail')
    line_id = fields.One2many('payments.receipt.details', 'prh_receipt_no', string='Line ID')

    @api.onchange('receipt_contract_id')
    def change(self):
        self.receipt_contract_code = self.receipt_contract_id.contract_code


class PaymentsReceiptDetails(models.Model):
    _name = 'payments.receipt.details'
    _description = 'รายละเอียดของใบเสร็จรับเงิน'
    _rec_name = 'prh_id'

    prh_id = fields.Integer(string='รหัส')
    prh_trans_code = fields.Integer(string='รหัสรายการ')
    prh_receipt_no = fields.Many2one('payments.receipt.headers', string='รหัสใบเสร็จ')
    prh_period = fields.Integer(string='งวดที่')
    prh_vat_rate = fields.Float(string='อัตราภาษีมูลค่าเพิ่ม')
    prh_amount = fields.Float(string='จำนวนเงิน')
    prh_total_amount = fields.Float(string='ยอดรวม')
    prh_vat_amount = fields.Float(string='จำนวนภาษีมูลค่าเพิ่ม')
    prh_tax_amount = fields.Float(string='จำนวนภาษี')
    prh_create_date = fields.Datetime(string='วันที่สร้างรายการ')
    prh_create_by = fields.Char(string='ผู้สร้างรายการ')
    prh_update_date = fields.Datetime(string='วันที่แก้ไขล่าสุด')
    prh_update_by = fields.Char(string='ผู้แก้ไขล่าสุด')
    prh_tax_rate = fields.Float(string='อัตราภาษี')
    prh_suspense_flag = fields.Boolean(string='สถานะ การ Suspense')
    prh_return_suspense_flag = fields.Boolean(string='สถานะ การ Return Suspense')
    prh_period_ef = fields.Integer(string='งวดที่ Ef')
    prh_dit_amt = fields.Float(string='ค่าขนส่ง')

    # head_id = fields.Many2one('payments.receipt.headers', string='Head ID')

    def action_open_account_move_wizard(self):
        # ดึงค่าจาก receipt_cust_name1 ของ payments.receipt.headers
        no = self.prh_receipt_no.receipt_contract_code

        # ตรวจสอบว่า `customer` เป็นชื่อหรือ ID ของ partner
        no_contract = self.env['account.move'].search([('receipt_contract_code', '=', no)])

        return {
            'name': 'แจ้งหนี้',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,  # เปิดด้วย view ที่กำหนด
            'res_id': no_contract.id,  # ส่ง id ของ account.move ที่ค้นหา
            'target': 'new',  # เปิดเป็น wizard
        }

