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

class TransferApprove(models.Model):
    _name = 'transfer.approve'

    date_from = fields.Datetime(string='วันที่โอนย้าย')
    date_to = fields.Datetime(string='ถึงวันที่')
    loan_type = fields.Selection([('สินเชื่อส่วนบุคคล', 'สินเชื่อส่วนบุคคล'), ('สินเชื่อเพื่อการศึกษา', 'สินเชื่อเพื่อการศึกษา'),
                                  ('สินเชื่อเพื่อรถยนต์', ' สินเชื่อเพื่อรถยนต์')], string='ประเภทสินเชื่อ')
    from_officer = fields.Many2one('hr.employee', string='จากเจ้าหน้าที่ติดตาม')
    to_officer = fields.Many2one('hr.employee', string='ถึงเจ้าหน้าที่ติดตาม')
    bucket = fields.Selection([('ปกติ', 'ปกติ'), ('Overdue1', 'Overdue1'), ('Overdue2', 'Overdue2')], string='Bucket')
    transfer_type = fields.Selection([('ระบุบุคคล', 'ระบุบุคคล')], string='ประเภทการโอนย้าย')
    area = fields.Selection([('กรุงเทพฯ', 'กรุงเทพ  ฯ')], string='พื้นที่')
    approve_result = fields.Selection([('อนุมัติ', 'อนุมัติ'), ('รออนุมัติ', 'รออนุมัติ')], string='ผลการอนุมัติ')
    no_loan = fields.Char(string='รหัสการโอนย้าย')
    line_id = fields.One2many('transfer.approve.line', 'head_id',  string='Line ID')

    def get_data(self):
        n = 1

class TransferApproveLine(models.Model):
    _name = 'transfer.approve.line'

    head_id = fields.Many2one('transfer.approve', string='Head ID')
    transfer_code = fields.Char(string='รหัสการโอนย้าย')
    transfer_date = fields.Datetime(string='วันที่โอนย้าย')
    transferor = fields.Many2one('hr.employee', string='ผู้โอนย้าย')
    type_transfer = fields.Selection([('ระบุบุคคล', 'ระบุบุคคล')], string='ประเภทการโอนย้าย')
    tracking_office = fields.Many2one('hr.employee', string='เจ้าหน้าที่ติดตาม ที่ได้รับการโอน')
    transfer_reason = fields.Char(string='เหตุผลการโอนย้าย')
    approve_result = fields.Char(string='ผลการอนุมัติ')
    approve_note = fields.Char(string='หมายเหตุการอนุมัติ')
    approver = fields.Many2one('hr.employee', string='ผู้อนุมัติ')
    date_approve = fields.Datetime(string='วันที่อนุมัติ')
    status = fields.Selection([('ใช้งาน', 'ใช้งาน'), ('ไม่ใช้งาน', 'ไม่ใช้งาน')], string='สถานะการใช้งาน')
