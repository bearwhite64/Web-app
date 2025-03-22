from odoo import api, fields, models

class Notice(models.Model):
    _name = 'notice'
    _description = 'Notice Information'

    letter_date_start = fields.Datetime(string='วันที่ออกจดหมาย',default=fields.Datetime.now)
    letter_date_end = fields.Datetime(string='ถึงวันทีออกจดหมาย',default=fields.Datetime.today)
    product_type = fields.Many2one('product.product', string='สินค้า')
    letter_type = fields.Selection(
        selection=[
            ('type1', 'ประเภทที่ 1'),
            ('type2', 'ประเภทที่ 2'),
            ('type3', 'ประเภทที่ 3'),
        ],
        string='ประเภทจดหมาย'
    )

    head_ids = fields.One2many('notice_detail', 'line_tree')

class NoticeDetail(models.Model):
    _name = 'notice_detail'
    _description = 'Notice Detail'

    no = fields.Char(string='ลำดับที่')
    letter_date_start_D = fields.Datetime(string='วันที่ออกจดหมาย', default=fields.Datetime.now)
    contract_number = fields.Char(string='เลขที่สัญญา')
    name_lessee = fields.Char(string='ชื่อ-นามสกุล(ผู้เช่าซื้อ)')
    address_lessee = fields.Char(string='ที่อยู่(ผู้เช่าซื้อ)')
    car_type = fields.Char(string='ประเภทรถ')
    car_brand = fields.Char(string='ยี่ห้อ')
    car_model = fields.Char(string='รุ่น')
    car_color = fields.Char(string='สี')
    engine_number = fields.Char(string='เลขตัวเครื่อง')
    chassis_number = fields.Char(string='เลขตัวถัง')

    line_tree = fields.Many2one('notice', string='notice_detail')