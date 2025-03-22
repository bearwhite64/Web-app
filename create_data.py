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

class CreateData(models.Model):
    _name = 'create.data'

    external_agency = fields.Char(string='หน่วยงานภายนอก')
    date_from = fields.Datetime(string='วันที่มอบหมายงาน')
    date_to = fields.Datetime(string='ถึงที่วัน')
    no_assign = fields.Char(string='รหัสการมอบหมายงาน')
    line_id = fields.One2many('create.data.line', 'head_id',  string='Line ID')

    def get_data(self):
        n = 1

class CreateDataLine(models.Model):
    _name = 'create.data.line'

    no_assign = fields.Char(string='รหัสการมอบหมายงาน')
    external_agency = fields.Char(string='หน่วยงานภายนอก')
    date_assign = fields.Datetime(string='วันที่มอบหมายงาน')
    head_id = fields.Many2one('create.data', string='Head ID')
