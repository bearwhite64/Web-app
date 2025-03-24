from odoo import api, fields, models

class master_data(models.Model):
    _name = 'master.data'
    _rec_name = 'name_bank1'
    _description = 'master data'


    bank_no = fields.Integer(string='เลขธนาคาร')
    name_bank1 = fields.Char(string='ชื่อธนาคาร')
    account_no1 = fields.Char(string='หมายเลขบัญชี', required=True, max_length=10)




# class contact_data(models.Model):
#     _name = 'contact.data'
#     _description = 'contact Data'
#
#     code1_m = fields.Many2one('code.p.m', string='รหัส')
    # กำหนดให้ name_bank เป็น Drop down ตัวเลือก แต่จะนำไปกำหนดเป็น Type Int,str ไม่ได้
    # name_bank = fields.Selection([
    #     ('Kbank', 'กสิกรไทย'),
    #     ('Scb', 'ไทยพาณิชย์'),
    #     ('KTB', 'กรุงไทย')
    # ], string='ชื่อธนาคาร')
    # bank_no = fields.Integer(string='เลขธนาคาร')
    # payment_m_type1 = fields.Selection([
    #     ('REV', 'Revenue'),
    #     ('EXP', 'Expense')
    # ], string='Payment Type')

    # description = fields.Selection([
    #     ('รายได้ค่าส่วนกลางรายเดือน', 'รายได้ค่าส่วนกลางรายเดือน'),
    #     ('รายรับแบบอื่นๆ', 'รายรับแบบอื่นๆ'),
    #     ('ค่าจ้าง รปภ', 'ค่าจ้าง รปภ'),
    #     ('ค่าไฟฟ้า', 'ค่าไฟฟ้า')
    # ], string='Description')



    # amount_m = fields.Float(string='จำนวนเงิน')
    # code2_m = fields.Integer('code1_m', string='รหัส')
    # serial_m = fields.Char(string='ประเภท')

    # เป็นการกำหนดเงื่อนไข ถ้า code_pay_m มีค่า 101 == 101 ให้แสดงรายการ code_name_m ที่กำหนดไว้ ออกมาพร้อมกับการเลือกรหัส 101,102,201,202
    # @api.onchange('code1_m', 'payment_m_type1')
    # def _onchange1_code(self):
    #     if self.payment_m_type1 == 'REV':
    #         if self.code1_m.code_pay_m == 101:
    #             self.serial_m = self.code1_m.code_name_m
    #         if self.code1_m.code_pay_m == 102:
    #             self.serial_m = self.code1_m.code_name_m
    #     elif self.payment_m_type1 == 'EXP':
    #         if self.code1_m.code_pay_m == 201:
    #             self.serial_m = self.code1_m.code_name_m
    #         if self.code1_m.code_pay_m == 202:
    #             self.serial_m = self.code1_m.code_name_m




    # code_name_m = fields.Char(string='รายการ')
    # code_pay_m = fields.Integer(string='รหัส')
    # amount_m = fields.Float(string='จำนวนเงิน')


# code_p_m
























