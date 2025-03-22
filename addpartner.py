from odoo import models, api, fields, _

class Addpartner(models.Model):
    _inherit = 'res.partner'

    name_eng = fields.Char(string='ชื่ออังกฤษ')
    id_card =  fields.Char(string='บัตรประชาชน')
    gender_part = fields.Selection(
        selection=[
            ('male', 'ชาย'),
            ('female', 'หญิง'),
            ('not_specified', 'ไม่ระบุ'),
            ('other', 'other')
        ],
        string="เพศ",
        default='other',  # ตั้งค่าเริ่มต้นเป็น 'ไม่ระบุ'
    )
    birth_part = fields.Date(string='วันเกิด')
    age_part = fields.Integer(string='อายุ',)
    ethnicity = fields.Char(string='เชื้อชาติ')
    nationality = fields.Char(string='สัญชาติ')
    occupation = fields.Char(string='อาชีพ', help='โปรดระบุอาชีพ')
    salary_part = fields.Float(string='เงินเดือน')

    type = fields.Selection(
        selection_add=[
            ('accordingcard', 'ที่อยู่ตามบัตรประชาชน'),
            ('workadd', 'ที่อยู่ที่ทำงาน'),
            ('accordinghouse', 'ที่อยู่ตามทะเบียนบ้าน/ภพ.20'),
        ],
        string='ประเภทที่อยู่'
    )
