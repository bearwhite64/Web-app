from odoo import models, fields

class ContactHistory(models.Model):
    _name = 'contact.history'
    _description = 'Contact History'

    date_info = fields.Datetime(string='วันที่และข้อมูล', required=True, default=fields.Datetime.now)
    created_by = fields.Char(string='ผู้ตั้งข้อมูล', required=True)
    record_code = fields.Char(string='รหัสบันทึก')
    follow_up_code = fields.Char(string='รหัสการติดตาม')
    follow_up_result = fields.Text(string='ผลการติดตาม')
    contact_person = fields.Char(string='ผู้ติดต่อ')
    special_status = fields.Selection([('ไม่มี', 'ไม่มี')], string='สถานะพิเศษ')
