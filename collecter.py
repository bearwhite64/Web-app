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

class TrackingResults(models.Model):
    _name = 'tracking.results'
    _description = 'ผลการติดตาม'

    name = fields.Char(string='ผู้บันทึกข้อมูล')
    results_no = fields.Char(string='รหัสบันทึก')
    results_contract = fields.Char(string='ผู้ติดต่อ')
    call_type = fields.Selection([
        ('pass_contract', 'อนุมัติโอนย้าย'),
        ('pay_failed', 'งานผิดนัดชำระ'),
        ('other', 'อื่นๆ'),
    ], string='รหัสติดตาม')
    contract_type = fields.Char(string='ประเภทผู้ติดต่อ')
    phone_number = fields.Char(string='เบอร์โทร')

    results = fields.Text(string='ผลการติดตาม')
    status_sp = fields.Char(string='สถานะพิเศษ')

    date_now = fields.Datetime(
        string="วันที่บันทึกข้อมูล",
        default=fields.Datetime.now  # ใช้วันที่และเวลาปัจจุบัน
    )
    head_line = fields.One2many('tracking.detail', 'line_ids', string='Head ID')

    start_time = fields.Datetime(string="Start Time")
    start_end = fields.Datetime(string="End Time")

    time_minute1 = fields.Integer(string='นาที', default=0)
    time_hour1 = fields.Integer(string='ชั่วโมง', default=0)

    @api.model
    def create(self, vals):
        # กำหนดค่า start_time เมื่อสร้างฟอร์ม
        if 'start_time' not in vals:
            vals['start_time'] = fields.Datetime.now()
        return super(TrackingResults, self).create(vals)

    def write(self, vals):
        # กำหนดค่า start_end เมื่อบันทึกฟอร์ม
        if 'start_end' not in vals:
            vals['start_end'] = fields.Datetime.now()

        return super(TrackingResults, self).write(vals)


    def action_save(self):
        # คำนวณเวลาใหม่และอัพเดทฟิลด์โดยตรง
        if self.start_time and self.start_end:
            start_time = fields.Datetime.from_string(self.start_time)
            start_end = fields.Datetime.from_string(self.start_end)

            # คำนวณเวลาที่ต่างกัน (diff) ในหน่วยวินาที
            diff = (start_end - start_time).total_seconds()

            # แปลงวินาทีเป็นนาทีและชั่วโมง
            minutes = diff // 60
            hours = minutes // 60
            minutes = minutes % 60  # นาทีที่เหลือหลังจากแปลงเป็นชั่วโมง

            # อัพเดทฟิลด์ time_minute1 และ time_hour1 โดยตรง
            self.write({
                'time_minute1': int(minutes),
                'time_hour1': int(hours)
            })

            # หาค่าล่าสุดของ tracking.detail ที่เชื่อมโยงกับ line_ids
            latest_tracking_detail = self.env['tracking.detail'].search([
                ('line_ids', '=', self.id)
            ], order='create_date desc', limit=1)

            # ถ้ามีข้อมูลล่าสุดใน tracking.detail
            if latest_tracking_detail:
                # อัพเดทฟิลด์ time_m และ time_h ใน tracking.detail
                latest_tracking_detail.write({
                    'time_m': int(minutes),
                    'time_h': int(hours)
                })
            else:
                # ถ้าไม่มี record ใน tracking.detail ให้ return True โดยไม่สร้าง record ใหม่
                return True

            # รีเซ็ต start_time และ start_end ให้เริ่มต้นใหม่
            self.write({
                'start_time': fields.Datetime.now(),
                'start_end': False,  # หรือกำหนดค่าเป็น None ก็ได้
                'time_minute1': 0,
                'time_hour1': 0,
            })

    @api.onchange('head_line')
    def _onchange_head_line(self):
        """อัพเดต num_time1 เมื่อเพิ่มไลน์ใน One2many"""
        for index, line in enumerate(self.head_line):
            line.num_time1 = index + 1  # อัพเดตลำดับให้เริ่มที่ 1 และเพิ่มทีละ 1

class TrackingResults1(models.Model):
    _name = 'tracking.detail'
    _description = 'รายละเอียดการติดตาม'

    num_time = fields.Char(string='ครั้งที่')
    num_time1 = fields.Integer(string='ครั้งที่')
    date_follow = fields.Date(string='วันที่ตาม')
    status_accord = fields.Char(string='รายละเอียดสถานะ')
    time_m = fields.Integer(string='นาที')
    time_h = fields.Integer(string='ชั่วโมง')
    line_ids = fields.Many2one('tracking.results', string='Line ID')

    # ฟังก์ชันนี้จะถูกเรียกเมื่อกดปุ่ม action_save

    # def action_save(self):
    #     # คำนวณเวลาใหม่และอัพเดทฟิลด์โดยตรง
    #     if self.start_time and self.start_end:
    #         start_time = fields.Datetime.from_string(self.start_time)
    #         start_end = fields.Datetime.from_string(self.start_end)
    #
    #         # คำนวณเวลาที่ต่างกัน (diff) ในหน่วยวินาที
    #         diff = (start_end - start_time).total_seconds()
    #
    #         # แปลงวินาทีเป็นนาทีและชั่วโมง
    #         minutes = diff // 60
    #         hours = minutes // 60
    #         minutes = minutes % 60  # นาทีที่เหลือหลังจากแปลงเป็นชั่วโมง
    #
    #         # อัพเดทฟิลด์ time_minute1 และ time_hour1 โดยตรง
    #         self.write({
    #             'time_minute1': int(minutes),
    #             'time_hour1': int(hours)
    #         })
    #
    #
    #         # สร้าง record ใหม่ใน tracking.detail (One2many)
    #         self.env['tracking.detail'].create({
    #             'num_time': format(len(self.head_line) + 1),  # นับจำนวนครั้งใน head_line
    #             'time_m': int(minutes),  # นาที
    #             'time_h': int(hours),  # ชั่วโมง
    #             'line_ids': self.id,  # เชื่อมโยงกับ ID ปัจจุบัน
    #         })
    #
    #         # รีเซ็ต start_time และ start_end ให้เริ่มต้นใหม่
    #         self.write({
    #             'start_time': fields.Datetime.now(),
    #             'start_end': False,  # หรือกำหนดค่าเป็น None ก็ได้
    #             'time_minute1': 0,
    #             'time_hour1': 0,
    #         })