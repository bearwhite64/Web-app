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

class JobTransferReport(models.Model):
    _name = 'job.transfer.report'

    date_from = fields.Datetime(string='วันที่ทำรายการ')
    date_to = fields.Datetime(string='ถึง')
    outstanding_installment = fields.Selection([('ปกติ', 'ปกติ'), ('Overdue', 'Overdue')], string='งวดค้างชำระ')
    manager = fields.Many2one('hr.employee', string='หัวหน้า')
    employee = fields.Many2one('hr.employee', string='พนักงาน',  domain="[('parent_id', '=', manager)]")
    line_id = fields.One2many('job.transfer.line', 'head_id',  string='Line ID')

    def get_data(self):
        n = 1

class TransferWorkLine(models.Model):
    _name = 'job.transfer.line'

    head_id = fields.Many2one('job.transfer.report', string='Head ID')
    no_contract = fields.Char(string='เลขที่สัญญา')
    no_customer = fields.Char(string='รหัสลูกค้า')
    name = fields.Char(string='ชื่อสกุล')
    old_collector = fields.Many2one('hr.employee', string='Collector เดิม')
    new_collector = fields.Many2one('hr.employee', string='Collector ใหม่')
    road = fields.Char(string='รหัสถนน')
    road_name = fields.Char(string='ชื่อถนน')
    no_zone = fields.Char(string='รหัส แขวง/ตำบล')
    name_zone = fields.Char(string='ชื่อ แขวง/ตำบล')
    out_balance = fields.Float(string='ยอดค้างชำระ')
    amount_out_balance = fields.Float(string='จำนวนนค้างชำระ')
    date_end = fields.Datetime(string='วันครบกำหนด')
    date_out_end = fields.Datetime(string='จำนวนวันที่เกินกำหนด')
