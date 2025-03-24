from odoo import models, fields, api

class Report_plan(models.Model):
    _name = 'report.p'
    _description = 'report Plan'

    # ข้อมูลหลัก
    name_sur = fields.Char(string='ผู้มีอำนาจ')
    name_project = fields.Char(string='ชื่อแผนงาน')
    corporation = fields.Char(string='หน่วยงานหรือแผนกที่สังกัด')
    job_pos = fields.Char(string='ตำแหน่ง')
    box_impact = fields.Boolean(string='การลดผลกระทบด้านสิ่งแวดล้อม')
    box_resources = fields.Boolean(string='การใช้ทรัพยากรอย่างมีประสิทธิภาพ')
    box_change = fields.Boolean(string='การปรับเปลี่ยนและเปลี่ยนแปลงสภาพภูมิอากาศ')
    box_protection = fields.Boolean(string='การป้องกันและฟื้นฟูธรรมชาติ')
    date_re = fields.Date(string='วันที่ประเมิณ')
    budget = fields.Float(string='งบประมาณ')
    purpose = fields.Char(string='วัตถุประสงค์')
    target = fields.Char(string='เป้าหมาย')
    metric = fields.Char(string='ตัวชี้วัด')

    # เชื่อมโยงข้อมูลกับ item1
    green_ids1 = fields.One2many('item1', 'item_id1', string='รายการการดำเนินงาน')
    green_ids2 = fields.One2many('item2', 'item_id2', string='ระยะคืนทุน')

    # @api.depends('green_ids2')
    # def _compute_green_ids2(self):
    #     # ลบข้อมูลใน item2 ที่มี item_id2 เดียวกัน
    #     records_to_delete = self.search([('item_id2', '=', self.item_id2.id)])
    #
    #     # เพิ่มข้อมูลใหม่
    #     for rec in self:
    #         # ดึงข้อมูลจาก green.factory มาใส่ใน item2
    #         rec.name2 = rec.item_id2.name_project
    #         rec.budget1_1 = rec.item_id2.budget
    #
    #         # เรียกใช้ฟังก์ชันเพื่อคำนวณ expenses2
    #         rec._compute_expenses2()
    #
    #     # เรียกใช้ฟังก์ชันคำนวณที่เกี่ยวข้อง
    #     self._compute_name2()
    #     self._compute_budget1_1()
    #
    #     return True


# ใช้งานได้
class Item_Check1(models.Model):
    _name = 'item1'
    _description = 'รายการการดำเนินงาน'

    item_id1 = fields.Many2one('green.factory', string='ID รายการ')
    # name = fields.Char(string='รายการ')
    name = fields.Selection([
        ('ค่าความร้อน', 'ค่าความร้อน'),
        ('จำนวนจุดที่เปลี่ยนท่อลมร้อน', 'จำนวนจุดที่เปลี่ยนท่อลมร้อน'),
        ('พลังงานไฟฟ้า', 'พลังงานไฟฟ้า'),
        ('ค่าไฟฟ้า', 'ค่าไฟฟ้า'),
        # ตารางที่ 2
        ('น้ำจากระบบหล่อเย็น', 'น้ำจากระบบหล่อเย็น'),
        ('ค่าน้ำประปา', 'ค่าน้ำประปา'),
        ('ค่าบำบัดน้ำเสีย', 'ค่าบำบัดน้ำเสีย'),

    ], string='name')  # ฟิลด์แบบ drop-down
    b_operating = fields.Float(string='ก่อนดำเนินงาน')
    a_operation = fields.Float(string='หลังดำเนินงาน')
    total = fields.Float(string='ประหยัดได้', compute='_compute_total_and_percen', store=True)
    percen = fields.Float(string='ร้อยละ %', compute='_compute_total_and_percen', store=True)
    unit = fields.Char(string='หน่วย')





    @api.depends('b_operating', 'a_operation', 'name')
    def _compute_total_and_percen(self):
        for record in self:
            if record.name == "พลังงานไฟฟ้า" :
                # คำนวณประหยัดได้ (b_operating - a_operation) สำหรับ "พลังงานไฟฟ้า"
                record.total = record.b_operating - record.a_operation if record.b_operating and record.a_operation else 0

                # คำนวณเปอร์เซ็นต์การประหยัด (total / b_operating) * 100
                if record.b_operating != 0:
                    record.percen = (record.total / record.b_operating) * 100
                else:
                    record.percen = 0

            elif record.name == "ค่าไฟฟ้า":
                # คำนวณประหยัดได้ (b_operating - a_operation) สำหรับ "ค่าไฟฟ้า"
                record.total = record.b_operating - record.a_operation if record.b_operating and record.a_operation else 0

                # ไม่คำนวณ percen สำหรับ "ค่าไฟฟ้า" ในกรณีนี้ให้เป็นศูนย์หรือไม่คำนวณ
                # record.percen = 0




class Item_Check2(models.Model):
    _name = 'item2'
    _description = 'คำนวณระยะคืนทุน'

    item_id2 = fields.Many2one('green.factory', string='ID รายการ', required=True)
    name2 = fields.Char(string='ชื่อโครงการ', compute='_compute_name2', store=True)
    budget1_1 = fields.Float(string='งบประมาณการลงทุน', compute='_compute_budget1_1', store=True)
    expenses2 = fields.Float(string='ค่าไฟฟ้าแผนงานที่ประหยัดได้', compute='_compute_expenses2', store=True)
    m_payback = fields.Float(string='ระยะคืนทุนรายเดือน', compute='_compute_payback', digits=(12, 2), store=True)
    y_payback = fields.Float(string='ระยะคืนทุนรายปี', compute='_compute_payback', digits=(12, 2), store=True)

    # @api.model
    def update_and_clear_data(self):
        # ลบข้อมูลใน item2 ที่มี item_id2 เดียวกัน
        records_to_delete = self.search([('item_id2', '=', self.item_id2.id)])
        records_to_delete.unlink()

        # เพิ่มข้อมูลใหม่
        for rec in self:
            # ดึงข้อมูลจาก green.factory มาใส่ใน item2
            rec.name2 = rec.item_id2.name_project
            rec.budget1_1 = rec.item_id2.budget

            # เรียกใช้ฟังก์ชันเพื่อคำนวณ expenses2
            rec._compute_expenses2()


        # เรียกใช้ฟังก์ชันคำนวณที่เกี่ยวข้อง
        self._compute_name2()
        self._compute_budget1_1()


        return True

        # แยกฟังก์ชันสำหรับการคำนวณชื่อและงบประมาณเพื่อทำให้โค้ดสะอาดขึ้น

    @api.depends('item_id2')
    def _compute_name2(self):
        for rec in self:
            rec.name2 = rec.item_id2.name_project if rec.item_id2 else ''

    @api.depends('item_id2')
    def _compute_budget1_1(self):
        for rec in self:
            rec.budget1_1 = rec.item_id2.budget if rec.item_id2 else 0.0

    @api.depends('item_id2.green_ids1')
    def _compute_expenses2(self):
        for rec in self:
            # ดึง total จาก item1 ที่มีรายการ "ค่าไฟฟ้า"
            total_expenses = sum(line.total for line in rec.item_id2.green_ids1 if line.name == "ค่าไฟฟ้า" )
            rec.expenses2 = total_expenses


    @api.depends('budget1_1', 'expenses2')
    def _compute_payback(self):
        for record in self:
            if record.expenses2 != 0:
                record.y_payback = round(record.budget1_1 / record.expenses2, 2)  # คำนวณระยะคืนทุนรายปี
                record.m_payback = round(record.y_payback * 12, 2)  # คำนวณระยะคืนทุนรายเดือน
            else:
                record.y_payback = 0
                record.m_payback = 0















