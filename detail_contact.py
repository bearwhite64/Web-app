from odoo import models, api, fields, _

class Detail_contactaddon(models.Model):
    _name = 'detail.contact.addon'

    no_contact = fields.Char(string='เลขที่สัญญา')
    cus_no = fields.Char(string='รหัสลูกค้า')
    name_borrower = fields.Char(string='ชื่อ (ผู้เช่าซื้อ / ผู้กู้)')
    citizen_code = fields.Char(string='เลขบัตรประชาชน')
    mobile_borrower = fields.Char(string='เบอร์ติดต่อ ผู้เช่าซื้อ / ผู้กู้')
    name_guarantor = fields.Char(string='ชื่อผู้ค้ำ')
    car_licenseplate = fields.Char(string='เลขทะเบียนรถ')
    carbrand = fields.Char(string='ยี่ห้อ/รุ่น')
    installment_month = fields.Char(string='ค่างวด/เดือน')
    term_payment = fields.Char(string='ขำระทุกวันที่')
    total_payment = fields.Integer(string='จำนวนงวดค้างชำระ')
    amount_payment = fields.Integer(string='จำนวนเงินค้างชำระ')
    amountdate_payment = fields.Integer(string='จำนวนวันค้างชำระ')
    latest_payment = fields.Date(string='วันที่ชำระล่าสุด')
    cutday = fields.Char(string='เงินรับชำระก่อนตัด')
    installment_latest = fields.Char(string='งวดชำระล่าสุด')
    contract_status = fields.Char(string='สถานะสัญญา')
    name_admin = fields.Char(string='พนักงานติมตาม')
    bukket = fields.Char(string='Bukket')