from odoo import models, fields, api
from datetime import datetime



class GreenAssessment(models.Model):
    _name = 'green.assessment'
    _description = 'หัวข้อผู้ประเมิน'

    green_ass1 = fields.One2many('assessment1', 'ass_line1', string='หัวหลัก')

    # ข้อมูลหลัก
    department = fields.Char(string='ฝ่าย/แผนก')
    location_work = fields.Char(string='พื้นที่กระบวนการผลิต')
    evaluation_of = fields.Char(string='การประเมินครั้งที่')
    assessor = fields.Char(string='ผู้ประเมิน')
    audit = fields.Char(string='ผู้ตรวจสอบ')

    date = fields.Date(string='วันที่ประเมิน', default=fields.Date.context_today)

    #แปลงค.ศ. เป็น พ.ศ. แบบนี้ก็ใช้ได้
    # @api.model
    # def create(self, vals):
    #     if 'date' in vals and vals['date']:
    #         # แปลงจาก ค.ศ. เป็น พ.ศ.
    #         date_obj = fields.Date.from_string(vals['date'])
    #         year_be = date_obj.year + 543  # คำนวณปี พ.ศ.
    #         # เก็บค่าที่แปลงในฟิลด์ date
    #         vals['date'] = date_obj.replace(year=year_be).strftime('%Y-%m-%d')  # เก็บในรูปแบบ ค.ศ.
    #     return super(GreenAssessment, self).create(vals)
    #
    # def write(self, vals):
    #     if 'date' in vals and vals['date']:
    #         # แปลงจาก ค.ศ. เป็น พ.ศ.
    #         date_obj = fields.Date.from_string(vals['date'])
    #         year_be = date_obj.year  # คำนวณปี พ.ศ.
    #         # เก็บค่าที่แปลงในฟิลด์ date
    #         vals['date'] = date_obj.replace(year=year_be).strftime('%Y-%m-%d')  # เก็บในรูปแบบ ค.ศ.
    #     return super(GreenAssessment, self).write(vals)

    @api.model
    def default_get(self, fields):
        res = super(GreenAssessment, self).default_get(fields)
        today = datetime.today()  # ใช้ datetime แทน date
        # แปลงปี ค.ศ. เป็น พ.ศ. (เพิ่ม 543 ปี)
        res['date'] = today.replace(year=today.year + 543).date()  # ใช้ .date() เพื่อคืนค่าเป็นฟิลด์ date
        return res




class Assessment1(models.Model):
    _name = 'assessment1'
    _description = "กรอกข้อมูล"

    ass_line1 = fields.Many2one('green.assessment', string='ID รายละเอียด')


    situation = fields.Selection([
        ('N', 'N'),
        ('A', 'A'),
        ('E', 'E'),
    ], string='สถานการณ์ N/A/E')

    cob_l1 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='โอกาสที่จะเกิด L1')

    cob_l2 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='โอกาสที่จะเกิด L2')

    violence_s1 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='ความรุนแรง S1')
    violence_s2 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='ความรุนแรง S2')
    violence_s3 = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='ความรุนแรง S3')

    point = fields.Integer(string='คะแนน', compute='_compute_point', store=True)

    @api.depends('cob_l1', 'cob_l2', 'violence_s1', 'violence_s2', 'violence_s3')
    def _compute_point(self):
        for rec in self:
            # ตรวจสอบว่าฟิลด์ที่เกี่ยวข้องมีค่าอยู่หรือไม่ ถ้าไม่มีให้ใช้ 0 แทน
            cob_l1 = int(rec.cob_l1) if rec.cob_l1 else 0
            cob_l2 = int(rec.cob_l2) if rec.cob_l2 else 0
            violence_s1 = int(rec.violence_s1) if rec.violence_s1 else 0
            violence_s2 = int(rec.violence_s2) if rec.violence_s2 else 0
            violence_s3 = int(rec.violence_s3) if rec.violence_s3 else 0

            # คำนวณค่า point
            rec.point = (cob_l1 + cob_l2) * (violence_s1 + violence_s2 + violence_s3)

    importance = fields.Selection([
        ('yes', 'มี'),
        ('no', 'ไม่มี'),
    ], string='นัยสำคัญ มี/ไม่มี')

    main1_ass = fields.Many2one('main1.assessment', string='ID กิจกรรม/ ผลิตภัณฑ์/ บริการ', default=lambda self: self._default_main1_ass())
    main2_ass = fields.Many2one('main2.assessment', string='ID ลักษณะปัญหา')
    main3_ass = fields.Many2one('main3.assessment', string='ID ผลกระทบ')

    @api.model
    def _default_main1_ass(self):
        # ดึงค่าล่าสุดของ name_work จาก main1.assessment
        last_main1_ass = self.env['main1.assessment'].search([], order="id desc", limit=1)
        if last_main1_ass:
            return last_main1_ass.id
        return None  # คืนค่า None ถ้ายังไม่มีข้อมูลใน main1.assessment





class Main1Assessment(models.Model):
    _name = 'main1.assessment'
    _rec_name = 'name_work'
    _description = 'กิจกรรม/ ผลิตภัณฑ์/ บริการ'

    name_work = fields.Char(string='กิจกรรม/ ผลิตภัณฑ์/ บริการ')


class Main2Assessment(models.Model):
    _name = 'main2.assessment'
    _rec_name = 'aspect'
    _description = 'ลักษณะปัญหา'

    aspect = fields.Char(string='ลักษณะปัญหา')




class Main3Assessment(models.Model):
    _name = 'main3.assessment'
    _rec_name = 'impact'
    _description = 'ผลกระทบ'

    impact = fields.Char(string='ผลกระทบ')