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

class TransferWork(models.Model):
    _name = 'assign.approve'
    _description ='มอบหมายงาน'

    external_agency = fields.Char(string='หน่วยงานภายนอก')
    admin = fields.Many2one('hr.employee', string='ผู้ดูแล')
    dispatcher = fields.Many2one('hr.employee', string='ผู้มอบหมายงาน')
    no_dispatcher = fields.Char(string='รหัสการมอบหมายงาน')
    date_assign_from = fields.Datetime(string='วันที่มอบหายงาน')
    date_assign_to = fields.Datetime(string='สิ้นสุด')
    date_end_from = fields.Datetime(string='วันที่หมดอายุ')
    date_end_to = fields.Datetime(string='สิ้นสุด')
    approve = fields.Selection([('รออนุมัติ', 'รออนุมัติ'), ('อนุมัติแล้ว', 'อนุมัติแล้ว')], string='ผลการอนุมัติ')
    line_id = fields.One2many('assign.work.line', 'head_id',  string='Line ID')

    def get_data(self):
        n = 1

class TransferWorkLine(models.Model):
    _name = 'assign.approve.line'

    head_id = fields.Many2one('assign.work', string='Head ID')
    assign_code = fields.Char(string='รหัสการมอบหมายงาน')
    external_agency = fields.Char(string='หน่วยงานภายนอก')
    assign_date = fields.Datetime(string='วันที่มอบหมายงาน')
    assign_date_count = fields.Datetime(string='จำนวนวันที่จะถึงวันหมดอายุ')
    assign_date_end = fields.Datetime(string='วันที่หมดอายุ')
    assigner = fields.Many2one('hr.employee', string='ผู้มอบหมายงาน')
    approve = fields.Selection([('รออนุมัติ', 'รออนุมัติ'), ('อนุมัติแล้ว', 'อนุมัติแล้ว')], string='ผลการอนุมัติ')
    record = fields.Many2one('hr.employee', string='ผู้ยันทึกข้อมูล')
    record_lastest = fields.Datetime(string='วันที่บันทึกล่าสุด')
    status = fields.Selection([('ใช้งาน', 'ใช้งาน'), ('ไม่ใช้งาน', 'ไม่ใช้งาน')], string='สถานะการใช้งาน')