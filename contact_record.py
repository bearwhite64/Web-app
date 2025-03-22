from odoo import models, fields, api

class ContactRecord(models.Model):
    _name = 'contact.record'
    _description = 'Contact Record'

    record_code = fields.Selection(
        [('option1', 'Option 1'), ('option2', 'Option 2')],
        string='รหัสบันทึก'
    )
    contact_person = fields.Char(string='ผู้ติดต่อ')
    follow_up_code = fields.Text(string='รหัสติดตาม')
    contact_type = fields.Selection(
        [('type1', 'ประเภทที่ 1'), ('type2', 'ประเภทที่ 2')],
        string='ประเภทผู้ติดต่อ'
    )
    phone_number = fields.Char(string='เบอร์โทร')
    appointment_date = fields.Datetime(string='เวลานัดหมาย')
    appointment_time = fields.Float(string='เวลานัดหมาย (ชั่วโมง)')
    follow_up_result = fields.Text(string='ผลการติดตาม')
    evaluation_status = fields.Selection(
        [('status1', 'สถานะ 1'), ('status2', 'สถานะ 2')],
        string='สถานะพิจารณา'
    )
