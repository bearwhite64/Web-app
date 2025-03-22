# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, api, fields, _

class ReportContract(models.Model):
    _name = 'report.account'

    manager = fields.Many2one('hr.employee', string='ผู้จัดการ')
    supervisor = fields.Many2one('hr.employee', string='หัวหน้างาน')
    employee_id = fields.Many2one('hr.employee', string='พนักงาน')

    head_ids = fields.One2many('report.account.details', 'line_ids', string='head ID')
    head_ids2 = fields.One2many('report.account.details2', 'line_ids2', string='head ID2')

    def action_search(self):
        records_data = [
            {"list_customer": "ล่วงหน้า", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ปกติ", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 1 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 2 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 3 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 4 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 5 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 6 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 7 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 8 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 9 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 10 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 11 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 12 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 13-18 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 19-24 งวด", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            {"list_customer": "ค้าง 25 งวดขึ้นไป", "no_of_cases": 0, "amount_due": 0.0, "remain_installments": 0.0},
            # เพิ่มอีก 16 records ตามต้องการ
        ]
        records_data2 = [
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},
            {"no_collected": 0, "receive_advance": 0.0, "remains_installments": 0.0},

        ]

        for data in records_data:
            self.head_ids.create({
                "line_ids": self.id,
                **data,
            })

        for data in records_data2:
            self.head_ids2.create({
                "line_ids2": self.id,
                **data,
            })



class ReportDetail(models.Model):
    _name = 'report.account.details'


    list_customer = fields.Char(string='รายการลูกหนี้')
    no_of_cases = fields.Integer(string='จำนวนรายที่มีให้เก็บ')
    amount_due = fields.Float(string='จำนวนเงินตามดิว')
    remain_installments = fields.Float(string='เงินค้างค่างวด')
    total_collect = fields.Float(string='รวมต้องเก็บ')
    remain_balance = fields.Float(string='ยอดลูกหนี้คงเหลือ')
    no_collected = fields.Integer(string='จำนวนรายที่เก็บได้')
    receive_advance = fields.Float(string='รับล่วงหน้า')
    remains_installments = fields.Float(string='จำนวนเงินค้างค่างวด')

    line_ids = fields.Many2one('report.account',string='line ID')




class ReportDetail2(models.Model):
    _name = 'report.account.details2'

    no_collected = fields.Integer(string='จำนวนรายที่เก็บได้')
    receive_advance = fields.Float(string='รับล่วงหน้า')
    remains_installments = fields.Float(string='จำนวนเงินค้างค่างวด')


    line_ids2 = fields.Many2one('report.account',string='line ID2')

#############################รายงาน performance######################################

class ReportPerformance(models.Model):
    _name = 'report.performance'

    date = fields.Date(string='วันที่ snap')
    manager = fields.Many2one('hr.employee', string='ผู้จัดการ')
    supervisor = fields.Many2one('hr.employee', string='หัวหน้า')
    employee_id = fields.Many2one('hr.employee', string='พนักงาน')
    product_sub = fields.Many2one('product.product',string='Sub Product')

    head_per = fields.One2many('performance.details', 'line_per', string='Head Per')
    head_per2 = fields.One2many('performance.details2', 'line_per2', string='Head Per2')

    @api.model
    def action_search(self):
        domain = []

        # ตรวจสอบค่าฟิลด์และเพิ่มเงื่อนไขไปยัง domain
        if self.product_sub:
            domain.append(('product_sub', '=', self.product_sub.id))

    @api.model
    def action_cancel(self):
        domain = []

        # ตรวจสอบค่าฟิลด์และเพิ่มเงื่อนไขไปยัง domain
        if self.product_sub:
            domain.append(('product_sub', '=', self.product_sub.id))


class ReportPerformanceDetails(models.Model):
    _name = 'performance.details'

    collector = fields.Char(string='collector')
    ac_total = fields.Float(string='A/C Total')
    ac_due = fields.Float(string='A/C Due')
    amt_due = fields.Float(string='Amt Due')
    amt_overdue = fields.Float(string='Amt OverDue')
    amt_total = fields.Float(string='Amt Total')
    ac_collect = fields.Char(string='A/C Collect')
    amt_collect_due = fields.Float(string='Amt Collect Due')
    amt_collect_overdue = fields.Float(string='Amt Collect Overdue')
    amt_collect_advance = fields.Float(string='Amt Collect Advance')


    line_per = fields.Many2one('report.performance', string='line_per')

class ReportPerformanceDetails2(models.Model):
    _name = 'performance.details2'

    ac_collect = fields.Char(string='A/C Collect')
    amt_collect_due = fields.Float(string='Amt Collect Due')
    amt_collect_overdue = fields.Float(string='Amt Collect Overdue')
    amt_collect_advance = fields.Float(string='Amt Collect Advance')
    amt_overdue = fields.Float(string='Amt OverDue')
    amt_total = fields.Float(string='Amt Total')

    line_per2 = fields.Many2one('report.performance', string='line_per2')

