from odoo import models, api, fields, _

class calculatepenalty(models.Model):
    _name = 'calculate.penalty'
    _description = 'คำนวณเบี้ยปรับ'

    start_receiv = fields.Date(string='วันที่จะรับค่างวด')
    end_receiv = fields.Date(string='วันที่เปิดสัญญา')
    final_installment = fields.Float(string='งวดสุดท้าย')
    outbalance = fields.Float(string='ยอดคงเหลือ')
    unpaid = fields.Float(string='ยอดค้างชำระ')
    taxes_unpaid = fields.Float(string='ภาษีค้างชำระ')
    stall = fields.Float(string='ค่างวด')
    taxes_stall = fields.Float(string='ภาษีค่างวด')
    totalstall = fields.Float(string='รวมค่างวด')
    penalty = fields.Float(string='ค่าเบี้ยปรับที่คำนวณ')
    total_num_stall = fields.Integer(string='จน.งวดทั้งหมด')
    demand_fee = fields.Float(string='ค่าทวงถาม')
    first_installment = fields.Date(string='งวดแรก')
    tracking_fee = fields.Float(string='ค่าติดตาม' ,default=0.0)
    total_num_pay = fields.Integer(string='จน.งวดที่จ่าย')
    total_num_overdue = fields.Integer(string='จน.งวดที่เกินกำหนด')
