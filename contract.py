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

class ContractDetails(models.Model):
    _name = 'contract.details'
    _description = 'รายละเอียดสัญญา'
    _rec_name = 'contract_id'

    contract_id = fields.Integer(string='เลขที่สัญญา ')
    contract_code = fields.Char(string='รหัสสัญญา')
    contract_customer_no = fields.Char(string='เลขลูกค้า')
    contract_customer_id = fields.Integer(string='รหัสลูกค้า')
    contract_loan_type = fields.Char(string='ประเภทสินเชื่อ')
    contract_loan_product_type = fields.Char(string='ประเภทสินเชื่อ (ย่อย)')
    contract_first_payment_date = fields.Date(string='วันที่ชำระเงินครั้งแรก')
    contract_close_date = fields.Datetime(string='วันที่ปิดสัญญา')
    contract_status = fields.Char(string='สถานะรายการ')
    contract_sub_status = fields.Char(string='สถานะย่อยรายการ')
    contract_comp_code = fields.Char(string='รหัสบริษัทของผู้ทำรายการ')
    contract_branch_code = fields.Char(string='รหัสสาขาของผู้ทำรายการ')
    contract_create_by = fields.Char(string='ผู้สร้างรายการ')
    contract_create_date = fields.Datetime(string='วันที่สร้างรายการ', default=fields.Datetime.now)
    contract_update_by = fields.Char(string='ผู้แก้ไขล่าสุด')
    contract_update_date = fields.Datetime(string='วันที่แก้ไขล่าสุด', default=fields.Datetime.now)
    contract_product_amount = fields.Float(string='ราคาสินค้า')
    contract_product_ex_vat_amount = fields.Float(string='ราคาสินค้าไม่รวมภาษี')
    contract_down_amount = fields.Float(string='ราคาดาวน์')
    contract_balloon_amount = fields.Float(string='ราคาบอลลูน')
    contract_total_period = fields.Integer(string='จำนวนงวด')
    contract_interest_rate_per_year = fields.Float(string='อัตราดอกเบี้ยต่อปี')
    contract_eff_rate = fields.Float(string='อัตราดอกเบี้ยแบบลดต้นลดดอกต่อปี')
    contract_eirr_rate = fields.Float(string='อัตราผลตอบแทน EIRR')
    contract_flag_due_beg_of_period = fields.Boolean(string='กำหนดจ่ายค่างวด')
    contract_installment_ex_vat_per_period = fields.Float(string='ค่างวดไม่รวมภาษิต่องวด')
    contract_installment_per_period = fields.Float(string='ค่างวดต่องวด')
    contract_vat_amount = fields.Float(string='ภาษี')
    contract_principal_amount = fields.Float(string='เงินต้น')
    contract_principal_ex_vat_amount = fields.Float(string='เงินต้นไม่รวมภาษี')
    contract_interest_amount = fields.Float(string='ดอกเบี้ย')
    contract_interest_ex_vat_amount = fields.Float(string='ดอกเบี้ยไม่รวมภาษี')
    contract_installment_total_amount = fields.Float(string='ค่างวดรวม')
    contract_stop_vat_flag_acc = fields.Boolean(string='สถานะหยุดนำส่งภาษี Acc')
    contract_stop_vat_date_acc = fields.Datetime(string='วันที่หยุดนำส่งภาษี Acc')
    contract_stop_accrue_flag_acc = fields.Boolean(string='สถานะหยุดรับรู้รายได้ Acc')
    contract_stop_accrue_date_acc = fields.Datetime(string='วันที่หยุดรับรู้รายได้ Acc')
    contract_stop_vat_flag_tax = fields.Boolean(string='สถานะหยุดนำส่งภาษี (Tax)')
    contract_stop_vat_date_tax = fields.Datetime(string='วันที่หยุดนำส่งภาษี (Tax)')
    contract_stop_accrue_flag_tax = fields.Boolean(string='สถานะหยุดรับรู้รายได้ (Tax)')
    contract_stop_accrue_date_tax = fields.Datetime(string='วันที่หยุดรับรู้รายได้ (Tax)')
    contract_write_off_flag = fields.Boolean(string='สถานะตัดหนี้สูญ')
    contract_write_off_date = fields.Date(string='วันที่ตัดหนี้สูญ')
    contract_write_off_amount = fields.Float(string='จำนวนที่ตัดหนี้สูญ')
    contract_flag_installment_ef = fields.Boolean(string='สถานะการจ่ายค่างวดแบบ EF')
    contract_flag_settlement = fields.Boolean(string='สถานะการปิดบัญชี')
    contract_settlement_date = fields.Datetime(string='วันที่ปิดบัญชี')
    contract_settle_cancel_date = fields.Datetime(string='วันที่ยกเลิก settle')
    contract_settlement_ref_code = fields.Char(string='รหัสอ้างอิงปิดบัญชีแบบ')
    contract_flag_reposs_settlement = fields.Boolean(string='สถานะการจ่ายเงินรถยึดแบบปิดบัญชี')
    contract_flag_reposs_current_period = fields.Boolean(string='สถานะการจ่ายเงินรถยึดแบบเคลียร์ทันงวด')
    contract_reposs_date = fields.Date(string='วันที่ยึดรถ')
    contract_payment_of_current_installment_success = fields.Boolean(string='สถานะการจ่ายเงินถึงงวดปัจจุบัน')
    contract_payment_of_current_installment_success_date = fields.Datetime(string='วันที่ชำระเงินถึงงวดปัจจุบัน')

class ContractInstallment(models.Model):
    _name = 'contract.installment'
    _description = 'รายละเอียดการผ่อนชำระ'
    _rec_name = 'install_id'

    install_id = fields.Integer(string='รหัสID')
    install_contract_id = fields.Many2one('contract.details',string='เลขที่สัญญา')
    install_contract_code = fields.Char(string='รหัสสัญญา')
    install_loan_type = fields.Char(string='ประเภทสินเชื่อ')
    install_first_due_date = fields.Date(string='วันที่กำหนดชำระครั้งแรก')
    install_next_due_date = fields.Date(string='วันที่กำหนดชำระครั้งถัดไป')
    install_last_paid_date = fields.Datetime(string='วันที่ทำการชำระครั้งล่าสุด')
    install_current_period = fields.Integer(string='งวดปัจจุบัน')
    install_end_period = fields.Integer(string='จำนวนงวดทั้งหมด')
    install_principal = fields.Float(string='จำนวนเงินต้น')
    install_principal_received = fields.Float(string='ยอดรับเงินต้น')
    install_interest = fields.Float(string='จำนวนดอกเบี้ย')
    install_interest_received = fields.Float(string='ยอดรับดอกเบี้ย')
    install_vat = fields.Float(string='ภาษี')
    install_vat_received = fields.Float(string='ยอดรับภาษี')
    install_fee_amount = fields.Float(string='ค่าธรรมเนียม')
    install_installment_ex_vat = fields.Float(string='งวดไม่รวมภาษี')
    install_installment_total_received = fields.Float(string='ยอดรับค่างวดรวม')
    install_installment_received = fields.Float(string='ยอดรับค่างวด')
    install_penalty_total_amount = fields.Float(string='จำนวนค่าปรับ')
    install_penalty_total_received = fields.Float(string='ยอดรับค่าปรับ')
    install_penalty_exceed_amount = fields.Float(string='ยอดรับชำระเบี้ยปรับเกิน')
    install_flag_stop_vat = fields.Boolean(string='สถานะ StopVat')
    install_status = fields.Char(string='สถานะรายการ')
    install_create_by = fields.Char(string='ผู้สร้างรายการ')
    install_create_date = fields.Datetime(string='วันที่สร้างรายการ')
    install_update_by = fields.Char(string='ผู้แก้ไขล่าสุด')
    install_update_date = fields.Datetime(string='วันที่แก้ไขล่าสุด')
    install_comp_code = fields.Char(string='รหัสบริษัทของผู้ทำรายการ')
    install_branch_code = fields.Char(string='รหัสสาขาของผู้ทำรายการ')
    install_flag_early_settlement = fields.Boolean(string='สถานะการปิดบัญชีก่อนกำหนด')
    install_early_settlement_date = fields.Date(string='วันที่ปิดบัญชีก่อนกำหนด')
    install_collection_note_date = fields.Date(string='วันที่ผิดสัญญา')
    install_installment_balance = fields.Float(string='ดอกเบี้ยคงเหลือ')
    install_principal_balance = fields.Float(string='เงินต้นคงเหลือ')
    install_interest_balance = fields.Float(string='ดอกเบี้ยคงเหลือ')
    install_vat_balance = fields.Float(string='ภาษีคงเหลือ')
    install_installment_ex_vat_balance = fields.Float(string='งวดไม่รวมภาษีคงเหลือ')
    install_fee_balance = fields.Float(string='ค่าธรรมเนียมคงเหลือ')
    install_stop_vat_date = fields.Datetime(string='วันที่หยุดนำส่งภาษี')
    install_next_period = fields.Integer(string='งวดถัดไป')
    install_loan_product_type = fields.Char(string='ประเภทสินเชื่อ (ย่อย)')
    line_id = fields.One2many('contract.installment.details', 'install_detail_insid', string='Line ID', required=True)

class ContractInstallmentDetails(models.Model):
    _name = 'contract.installment.details'
    _description = 'รายละเอียดการผ่อนชำระแต่ละงวด'
    _rec_name = 'install_detail_id'

    install_detail_id = fields.Integer(string='รหัสของ InsD')
    install_detail_insid = fields.Many2one('contract.installment',string='รหัสผ่อนชำระ')
    install_detail_contract_id = fields.Many2one('contract.details',string='รหัสสัญญา')
    install_detail_contract_code = fields.Char(string='รหัสสัญญา')
    install_detail_last_paid_date = fields.Datetime(string='วันที่ชำระล่าสุด')
    install_detail_period = fields.Integer(string='งวดที่')
    install_detail_due_date = fields.Datetime(string='วันที่กำหนดชำระ')
    install_detail_principal = fields.Float(string='เงินต้น')
    install_detail_principal_received = fields.Float(string='ยอดรับเงินต้น')
    install_detail_interest = fields.Float(string='ดอกเบี้ย')
    install_detail_interest_received = fields.Float(string='ยอดรับดอกเบี้ย')
    install_detail_vat = fields.Float(string='ภาษี')
    install_detail_vat_received = fields.Float(string='ยอดรับภาษี')
    install_detail_fee_amount = fields.Float(string='ค่าธรรมเนียม')
    install_detail_fee_received = fields.Float(string='ยอดรับค่าธรรมเนียม')
    install_detail_installment_ex_vat = fields.Float(string='ค่างวดไม่รวมภาษี')
    install_detail_installment_ex_vat_received = fields.Float(string='ยอดรับค่างวดไม่รวมภาษี')
    install_detail_installment_total = fields.Float(string='ยอดเงินค่างวด')
    install_detail_installment_received = fields.Float(string='ยอดรับค่างวด')
    install_detail_penalty_amount = fields.Float(string='ค่าปรับ')
    install_detail_penalty_received = fields.Float(string='ยอดรับค่าปรับ')
    install_detail_flag_match = fields.Boolean(string='สถานะ การ Match')
    install_detail_status = fields.Char(string='สถานะรายการ')
    install_detail_create_by = fields.Char(string='ผู้สร้างรายการ')
    install_detail_create_date = fields.Datetime(string='วันที่สร้างรายการ')
    install_detail_update_by = fields.Char(string='ผู้แก้ไขล่าสุด')
    install_detail_update_date = fields.Datetime(string='วันที่แก้ไขล่าสุด')
    install_detail_comp_code = fields.Char(string='รหัสบริษัทของผู้ทำรายการ')
    install_detail_branch_code = fields.Char(string='รหัสสาขาของผู้ทำรายการ')
    install_detail_flag_gen_invoice_hp = fields.Boolean(string='สถานะการ Gen Invoice สัญญาเช่าซื้อ')
    install_detail_installment_balance = fields.Float(string='ค่างวดคงเหลือ')
    install_detail_principal_balance = fields.Float(string='เงินต้นคงเหลือ')
    install_detail_interest_balance = fields.Float(string='ดอกเบี้ยคงเหลือ')
    install_detail_vat_balance = fields.Float(string='ภาษีคงเหลือ')
    install_detail_installment_ex_vat_balance = fields.Float(string='ค่างวดไม่รวมภาษีคงเหลือ')
    install_detail_fee_balance = fields.Float(string='ค่าธรรมเนียมคงเหลือ')
    install_detail_match_by = fields.Char(string='Match โดย')
    install_detail_match_date = fields.Datetime(string='วันที่ Match')
    install_detail_principal_amt = fields.Float(string='จำนวนเงินต้นทั้งหมด')
    head_id = fields.Many2one('contract.installment', string='Head ID', required=True)