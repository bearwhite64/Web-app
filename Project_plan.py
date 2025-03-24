from odoo import models, fields, api

class Green_factory(models.Model):
    _name = 'green.factory'
    _description = 'Green factory'

    # ข้อมูลหลัก

    name_sur = fields.Char(string='ชื่อ-นามสกุล')
    name_project = fields.Char(string='ชื่อแผนงาน')
    corporation = fields.Char(string='หน่วยงานหรือแผนกที่สังกัด')
    job_pos = fields.Char(string='ตำแหน่ง')
    box_impact = fields.Boolean(string='การลดผลกระทบด้านสิ่งแวดล้อม')
    box_resources = fields.Boolean(string='การใช้ทรัพยากรอย่างมีประสิทธิภาพ')
    box_change = fields.Boolean(string='การปรับเปลี่ยนและเปลี่ยนแปลงสภาพภูมิอากาศ')
    box_protection = fields.Boolean(string='การป้องกันและฟื้นฟูธรรมชาติ')
    start_date = fields.Date(string='ระยะเวลาดำเนินการเริ่มต้น')
    end_date = fields.Date(string='ระยะเวลาดำเนินการสิ้นสุด')
    budget = fields.Float(string='งบประมาณ', default=0)
    purpose = fields.Char(string='วัตถุประสงค์')
    target = fields.Char(string='เป้าหมาย')
    metric = fields.Char(string='ตัวชี้วัด')

    # เชื่อมโยงข้อมูลกับ item1
    green_ids1 = fields.One2many('item1', 'item_id1', string='รายการการดำเนินงาน')
    green_ids2 = fields.One2many('item2', 'item_id2', string='ระยะคืนทุน')
    green_ids3 = fields.One2many('item3', 'item_id3', string='การคำนวณก๊าซเรือนกระจก')

    #ปุ่ม link เข้าอีก Grantchart
    def action_open_gantt_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gantt View',
            'view_mode': 'gantt',
            'res_model': 'project.task',
            'views': [(self.env.ref('ls_project_timeline_gantt.project_task_dependency_view_gantt').id, 'gantt')],
            'target': 'current',
        }

# ใช้งานได้
class Item_Check1(models.Model):
    _name = 'item1'
    _description = 'รายการการดำเนินงาน'

    item_id1 = fields.Many2one('green.factory', string='ID รายการ')
    # name = fields.Char(string='รายการ')
    name = fields.Selection([
        # โครงการที่1
        ('ค่าความร้อน', 'ค่าความร้อน'),
        ('จำนวนจุดที่เปลี่ยนท่อลมร้อน', 'จำนวนจุดที่เปลี่ยนท่อลมร้อน'),
        ('พลังงานไฟฟ้า', 'พลังงานไฟฟ้า'),
        ('ค่าไฟฟ้า', 'ค่าไฟฟ้า'),
        # โครงการที่2
        ('น้ำจากระบบหล่อเย็น', 'น้ำจากระบบหล่อเย็น'),
        ('ค่าน้ำประปา', 'ค่าน้ำประปา'),
        ('ค่าบำบัดน้ำเสีย', 'ค่าบำบัดน้ำเสีย'),
        # โครงการที่3
        ('น้ำมันตัดเหล็กผสมน้ำต้องกำจัด', 'น้ำมันตัดเหล็กผสมน้ำต้องกำจัด'),


    ], string='name')  # ฟิลด์แบบ drop-down
    b_operating = fields.Float(string='ก่อนดำเนินงาน', default=0)
    a_operation = fields.Float(string='หลังดำเนินงาน', default=0)
    total = fields.Float(string='ประหยัดได้', compute='_compute_total_and_percen', store=True)
    total1 = fields.Float(string='ประหยัดได้', compute='_compute_total_and_percen', store=True)
    total2 = fields.Float(string='ประหยัดได้', compute='_compute_total_and_percen', store=True)
    percen = fields.Float(string='ร้อยละ %', compute='_compute_total_and_percen', store=True)
    unit = fields.Char(string='หน่วย')
    b_operating1 = 0
    a_operation1 = 0




    # Fucntion สร้างเงื่อนไข จากการดึง id ที่มีชื่อที่กำหนด และเอาค่าที่ได้จาก ตัวนั้นมาคำนวณหาค่าต่อ
    @api.depends('b_operating', 'a_operation', 'name')
    def _compute_total_and_percen(self):
        for record in self:
            # โครงการที่1 หา name == "พลังงานไฟฟ้า" โดยรับค่าจากข้อมูลที่เข้ามาที่ b_operating และ a_operation ลบกัน เพื่อไปเก็บใน total
            if record.name == "พลังงานไฟฟ้า":
                # คำนวณประหยัดได้ (b_operating - a_operation) สำหรับ "พลังงานไฟฟ้า"
                record.total = record.b_operating - record.a_operation

                # นำค่า total ที่หาได้แล้ว เพื่อคำนวณต่อ ไปเก็บไว้ใน percen โดยที่ค่าเข้ามาของ b_operating ไม่เท่ากับ 0 เพื่อกันไม่ให้ไปหารและได้ค่า 0
                # คำนวณเปอร์เซ็นต์การประหยัด (total / b_operating) * 100
                if record.b_operating != 0:
                    record.percen = (record.total / record.b_operating) * 100
                else:
                    record.percen = 0

            if record.name == "ค่าไฟฟ้า":
                # คำนวณประหยัดได้ (b_operating - a_operation) สำหรับ "ค่าไฟฟ้า"
                record.total = record.b_operating - record.a_operation

            # โครงการที่2
            if record.name == "น้ำจากระบบหล่อเย็น":
                record.total = record.b_operating - record.a_operation

                if record.b_operating != 0:
                    record.percen = (record.total / record.b_operating) * 100
                else:
                    record.percen = 0

            if record.name == "ค่าน้ำประปา":
                # คำนวณประหยัดได้ (b_operating - a_operation) สำหรับ
                record.total = record.b_operating - record.a_operation
                record.total1 = record.total

            if record.name == "ค่าบำบัดน้ำเสีย":
                # คำนวณประหยัดได้ (b_operating - a_operation) สำหรับ
                record.total = record.b_operating - record.a_operation
                record.total2 = record.total

            # โครงการที่3 หา name == "น้ำมันตัดเหล็กผสมน้ำต้องกำจัด" เป็นการรับค่ามาและนำไปคำนวณก่อน
            # จะนำไปใช้ใจการคำนวณจริงอีกครั้ง โดยนำค่าที่ได้ไปเก็บไว้ใน ตัวแปรลอย b_operating1,a_operation1
            # นำค่าที่เก็บไว้ในตัวแปรลอย เอาค่ามาลบกัน เพื่อเก็บค่าที่ต้องการลงใน total
            if record.name == "น้ำมันตัดเหล็กผสมน้ำต้องกำจัด":
                b_operating1 = ((record.b_operating * 1000000) * 0.898) / 1000
                a_operation1 = ((record.a_operation * 1000000) * 0.898) / 1000
                record.total = b_operating1 - a_operation1





class Item_Check2(models.Model):
    _name = 'item2'
    _description = 'คำนวณระยะคืนทุน'

    item_id2 = fields.Many2one('green.factory', string='ID รายการ', required=True)
    name2 = fields.Char(string='ชื่อโครงการ', compute='_compute_name2', store=True)
    budget1_1 = fields.Float(string='งบประมาณการลงทุน', compute='_compute_budget1_1', store=True)
    expenses2 = fields.Float(string='แผนงานที่ประหยัดได้', compute='_compute_expenses2', store=True)
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

    # Function ดึงข้อมูลชื่อ name_project ใน class Master มาเก็บไว้ใน name2 ใน class ตัวเอง
    @api.depends('item_id2')
    def _compute_name2(self):
        for rec in self:
            rec.name2 = rec.item_id2.name_project if rec.item_id2 else ''

    # Function ดึงข้อมูลงบประมาณจาก budget ใน class Master มาเก็บไว้ใน budget1_1
    @api.depends('item_id2')
    def _compute_budget1_1(self):
        for rec in self:
            rec.budget1_1 = rec.item_id2.budget if rec.item_id2 else 0.0

    # Function ต้องการผลรวมของ ค่าไฟฟ้า โดยไปเรียกข้อมูล ชื่อจาก item1 ที่มี id เดียวกันมาเรียกใช้
    @api.depends('item_id2.green_ids1')
    def _compute_expenses2(self):
        for rec in self:
            # คำนวณค่าใช้จ่าย โครงการที่ 1
            total_expenses = 0  # เริ่มต้นที่ 0
            for line in rec.item_id2.green_ids1:
                if line.name == "ค่าไฟฟ้า":  # ตรวจสอบชื่อ
                    total_expenses += line.total  # รวมค่าใช้จ่ายของ "ค่าไฟฟ้า"

            # ตรวจสอบเงื่อนไขอื่น ๆ โครงการที่ 2
            if total_expenses != 0:
                self.expenses2 = total_expenses
            else:
                # ใช้ข้อมูลเรียกเก็บตัวแปรลอยให้คำนวณ
                plus = 0
                minus = 0
                for line in rec.item_id2.green_ids1:
                    plus += line.total1
                    minus += line.total2
                balance = plus + minus
                self.expenses2 = balance


    # เป็น Fucntion ที่เรียกข้อมูล budget1_1 และ expenses2 ใน class มาเข้าสูตร เพื่อคำนวณต่อ
    @api.depends('budget1_1', 'expenses2')
    def _compute_payback(self):
        for record in self:
            if record.expenses2 != 0:
                record.y_payback = round(record.budget1_1 / record.expenses2, 2)  # คำนวณระยะคืนทุนรายปี
                record.m_payback = round(record.y_payback * 12, 2)  # คำนวณระยะคืนทุนรายเดือน
            else:
                record.y_payback = 0
                record.m_payback = 0

class Item_Check3(models.Model):
    _name = 'item3'
    _description = 'การคำนวณก๊าซเรือนกระจก'

    item_id3 = fields.Many2one('green.factory', string='ID รายการ', required=True)
    name3 = fields.Char(string='ชื่อโครงการ', compute='_compute_name3', store=True)
    expenses3 = fields.Float(string='กิโลกรัมต่อปี', compute='_compute_expenses3', store=True)
    emission_factor = fields.Float(string='ค่าก๊าซเรือนกระจก',digits=(12, 4),default=0)
    dioxide = fields.Float(string='กิโลกรัมคาร์บอนไดออกไซด์', compute='_compute_dioxide', store=True, digits=(12, 3))

    def update_and_clear_data1(self):
        # ลบข้อมูลใน item3 ที่มี item_id3 เดียวกัน
        records_to_delete1 = self.search([('item_id3', '=', self.item_id3.id)])
        records_to_delete1.unlink()

        # เพิ่มข้อมูลใหม่
        for rec in self:
            # ดึงข้อมูลจาก green.factory มาใส่ใน item3
            rec.name3 = rec.item_id3.name_project

            # เรียกใช้ฟังก์ชันเพื่อคำนวณ expenses3
            rec._compute_expenses3()


        # เรียกใช้ฟังก์ชันคำนวณที่เกี่ยวข้อง
        self._compute_name3()

        return True

    # เป็นการเรียกข้อมูล name_project ที่อยู่ใน class green.factory มาเก็บไว้ใน name3 ี่อยู่ใน class item3
    @api.depends('item_id3')
    def _compute_name3(self):
        for rec in self:
            rec.name3 = rec.item_id3.name_project if rec.item_id3 else ''

    # เป็นการดึงค่า total จาก class item1 โดยดึงจาก id ที่เชื่อมกับ class green.factory ที่เป็น Master
    # เรียกค่า total มาใช้ให้มาเก็บลงใน expenses3 ที่อยู่ใน class item3
    @api.depends('item_id3.green_ids1')
    def _compute_expenses3(self):
        for rec in self:
            # คำนวณค่าใช้จ่าย โครงการที่ 1
            total_expenses3 = 0  # เริ่มต้นที่ 0
            for line in rec.item_id3.green_ids1:
                if line.name == "น้ำมันตัดเหล็กผสมน้ำต้องกำจัด":  # ตรวจสอบชื่อ
                    total_expenses3 += line.total  # รวมค่าใช้จ่ายของ "ค่าไฟฟ้า"
            #
            # ตรวจสอบเงื่อนไขอื่น ๆ โครงการที่ 2
                if total_expenses3 != 0:
                    self.expenses3 = total_expenses3

# ฟังก์ชันคำนวณ dioxide การดึงค่าที่ได้จาก expenses3 * emission_factor = dioxide
    @api.depends('expenses3', 'emission_factor')
    def _compute_dioxide(self):
        for rec in self:
            # คำนวณ dioxide = expenses3 * emission_factor
            rec.dioxide = rec.expenses3 * rec.emission_factor












