from odoo import models, api, fields, _

class Contactrecord(models.Model):
    _name = 'contract.record'

    code_record = fields.Char(string='รหัสบันทึก')
    communicant = fields.Char(string='ผู้ติดต่อ')
    code_trace = fields.Char(string='รหัสติดตตาม')
    type_person = fields.Char(string='ประเภทผู้ติดต่อ')
    phone = fields.Char(string='เบอร์โทร')
    time = fields.Datetime(string='เวลานัดหมาย')
    tracking_results = fields.Text(string='ผลการติดตาม')
    status = fields.Char(string='สถานะพิเศษ')
