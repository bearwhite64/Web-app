from odoo import api, fields, models, _


class payment_data(models.Model):
    _name = 'payment.data'
    _description = 'payment Data'

    name = fields.Char(string='ชื่อ')
    # bank = fields.Selection([
    #     ('Kbank', 'กสิกรไทย'),
    #     ('Scb', 'ไทยพาณิชย์'),
    #     ('KTB', 'กรุงไทย')
    # ], string='ธนาคาร')
    house_no = fields.Char(string='บ้านเลขที่')

    date = fields.Date(string='วันที่', default=fields.Date.context_today)



    mas_in = fields.Many2one('master.data', string='ธนาคาร' )

    line_in = fields.One2many('pay.linein', 'pay_in', string='LINE Messages')
    # line_in2 = fields.One2many('contact.data', 'payment_p_id', string='LINE Messages')
    # , 'contact.data'

class payment_payment(models.Model):
    _name = 'pay.linein'
    _description = 'pay linein'

    pay_in = fields.Many2one('payment.data', string='Payment_in')
    # pay_in2 = fields.One2many('contact.data','payment_line_id', string='Payment_in')
    # , 'contact.data'
    payment_type = fields.Selection([
        ('REV', 'Revenue'),
        ('EXP', 'Expense')
    ], string='Payment Type')

    # code = fields.Selection([
    #     ('101', '101'),
    #     ('102', '102'),
    #     ('201', '201'),
    #     ('202', '202')
    # ], string='รหัส')


    amount = fields.Float(string='จำนวนเงิน')
    code1 = fields.Many2one('code.p', string='รายการ')
    # serial = fields.Many2one('code.p', string='รหัส')
    # serial = fields.Char(string='ประเภท')

    # @api.onchange('code1', 'payment_type')
    # def _onchange_code(self):
    #     if self.payment_type == 'REV':
    #         if self.code1.code_pay == 101:
    #             self.amount = self.code1.amount
    #             self.serial = self.code1.code_name
    #         if self.code1.code_pay == 102:
    #             self.serial = self.code1.code_name
    #             self.amount = self.code1.amount
    #     elif self.payment_type == 'EXP':
    #         if self.code1.code_pay == 201:
    #             self.serial = self.code1.code_name
    #             self.amount = self.code1.amount
    #         if self.code1.code_pay == 202:
    #             self.serial = self.code1.code_name
    #             self.amount = self.code1.amount

class code_p(models.Model):
    _name = 'code.p'
    _rec_name = 'code_name'
    _description = 'code'

    # code_in = fields.One2many('contact.data', 'payment_c_id', string='Payment_in')
    code_name = fields.Char(string='รายการ')
    code_pay = fields.Integer(string='รหัส')
    amount = fields.Float(string='จำนวนเงิน')

    # bank_no = fields.Integer(string='เลชธนาคาร')
