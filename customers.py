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

class MsCustormerDetails(models.Model):
    _name = 'ms.custormer.details'
    _rec_name = 'customer_id'

    customer_id = fields.Integer(string='รหัสลูกค้า')
    user_brance_id = fields.Char(string='รหัสสาขาผู้ใช้')
    customer_code = fields.Char(string='รหัสลูกค้า')
    identity_no = fields.Char(string='เลขที่บัตรแสดงตน')
    id_card_no = fields.Char(string='เลขที่บัตรประชาชน')
    issue_date = fields.Date(string='วันที่ออกบัตร')
    issue_by = fields.Char(string='ผู้ออกบัตร')
    expire_date = fields.Date(string='วันหมดอายุ')
    first_name = fields.Char(string='ชื่อ')
    last_name = fields.Char(string='นามสกุล')
    birthdate = fields.Date(string='วันเกิด')
    tax_no = fields.Char(string='เลขประจำตัวผู้เสียภาษี')
    registration_no = fields.Char(string='หมายเลขจดทะเบียน')
    registration_date = fields.Date(string='วันที่จดทะเบียน')
    employee_amount = fields.Integer(string='จำนวนพนักงาน')
    registered_capital = fields.Float(string='ทุนจดทะเบียน')
    active = fields.Boolean(string='สถานะการใช้งาน')
    create_by = fields.Char(string='ผู้สร้าง')
    create_date = fields.Datetime(string='วันที่สร้าง')
    update_by = fields.Char(string='ผู้แก้ไข')
    update_date = fields.Datetime(string='วันที่แก้ไข')
    business_type_id = fields.Char(string='ประเภทธุรกิจ')
    detail = fields.Char(string='รายละเอียด')
    execution_date = fields.Datetime(string='วันที่เริ่มดำเนินการ')
    paid_in_capital = fields.Float(string='ทุนชำระแล้ว')
    remark = fields.Char(string='หมายเหตุ')
    comp_code = fields.Char(string='รหัสบริษัท')
    comp_branch_code = fields.Char(string='รหัสสาขา')
    nick_name = fields.Char(string='ชื่อเล่น')
    lifetime_flag = fields.Boolean(string='บัตรประชาชนตลอดชีพ')
    photo_in_card = fields.Text(string='รูปบัตรประชาชน')
    edit_status = fields.Char(string='สถานะแก้ไข')

    customer_group_id = fields.Many2one('m.cus.group',string='รหัสกลุ่มลูกค้า')
    customer_type_id = fields.Many2one('m.cus.type',string='รหัสสาขาผู้ใช้')
    title_id = fields.Many2one('m.title.id',string='รหัสคำนำหน้า')
    gender_id = fields.Many2one('m.gender.id',string='รหัสเพศ')
    identity_type_id = fields.Many2one('m.identity.id',string='รหัสประเภทบัตรแสดงตน')
    education_id = fields.Many2one('m.education.id',string='รหัสการศึกษา')
    marital_status_id = fields.Many2one('m.marital.id',string='รหัสสถานภาพสมรส')
    race_id = fields.Many2one('m.race.id',string='รหัสสถานภาพสมรส')
    nationality_id = fields.Many2one('m.nationality.id',string='รหัสสถานภาพสมรส')




class CustormerGroup(models.Model):
    _name = 'm.cus.group'
    _rec_name = 'group_detail'

    group_no = fields.Char(string='group')
    group_detail = fields.Char(string='customer_group')

class CustormerType(models.Model):
    _name = 'm.cus.type'
    _rec_name = 'cus_detail'

    cus_no = fields.Char(string='cus')
    cus_detail = fields.Char(string='detail')

class TitleID(models.Model):
    _name = 'm.title.id'
    _rec_name = 'title_detail'

    cus_no = fields.Char(string='type')
    title_detail = fields.Char(string='detail')

class GenderID(models.Model):
    _name = 'm.gender.id'
    _rec_name = 'gender_detail'


    gender_no = fields.Char(string='gender')
    gender_detail = fields.Char(string='detail')

class IdentityID(models.Model):
    _name = 'm.identity.id'
    _rec_name = 'identity_detail'

    identity_no = fields.Char(string='identity')
    identity_detail = fields.Char(string='detail')

class EducationID(models.Model):
    _name = 'm.education.id'
    _rec_name = 'education_detail'

    education_no = fields.Char(string='education')
    education_detail = fields.Char(string='detail')

class MaritalID(models.Model):
    _name = 'm.marital.id'
    _rec_name = 'marital_detail'

    marital_no = fields.Char(string='marital')
    marital_detail = fields.Char(string='detail')

class RaceID(models.Model):
    _name = 'm.race.id'
    _rec_name = 'race_detail'

    race_no = fields.Char(string='race')
    race_detail = fields.Char(string='detail')

class NationalityID(models.Model):
    _name = 'm.nationality.id'
    _rec_name = 'nationality_detail'

    nationality_no = fields.Char(string='race')
    nationality_detail = fields.Char(string='detail')

class CustomerAddress(models.Model):
    _name = 'ms.custormer.address'
    _description = 'ที่อยู่ของลูกค้า'
    _rec_name = 'address_id'

    address_id = fields.Integer(string='รหัสที่อยู่')
    customer_id = fields.Many2one('ms.custormer.details', string='ลูกค้า')
    address_type_id = fields.Char(string='ประเภทที่อยู่')
    province_code = fields.Char(string='รหัสจังหวัด')
    district_code = fields.Char(string='รหัสอำเภอ')
    subdistrict_code = fields.Char(string='รหัสตำบล')
    zipcode_code = fields.Integer(string='รหัสไปรษณีย์')
    living_status_id = fields.Char(string='สถานภาพการอยู่อาศัย')
    house_no = fields.Char(string='เลขที่')
    village_no = fields.Char(string='หมู่ที่')
    village_name = fields.Char(string='หมู่บ้าน/อาคาร')
    floor = fields.Char(string='ชั้น')
    room_no = fields.Char(string='ห้อง')
    soi = fields.Char(string='ซอย')
    road = fields.Char(string='ถนน')
    living_at = fields.Char(string='ปีที่เข้าอยู่')
    living_time = fields.Char(string='อาศัยมานาน')
    house_reg_no = fields.Char(string='หมายเลขบ้าน')
    tel = fields.Char(string='โทรศัพท์')
    fax = fields.Char(string='โทรสาร')
    remark = fields.Text(string='หมายเหตุ')
    active = fields.Boolean(string='สถานะการใช้งาน')
    create_by = fields.Char(string='ผู้สร้าง')
    create_date = fields.Datetime(string='วันที่สร้าง')
    update_by = fields.Char(string='ผู้แก้ไข')
    update_date = fields.Datetime(string='วันที่แก้ไข')
    comp_code = fields.Char(string='รหัสบริษัท')
    comp_branch_code = fields.Char(string='รหัสสาขาบริษัท')
    latitude = fields.Float(string='ละติจูด')
    longitude = fields.Float(string='ลองจิจูด')

class CustomerOccupation(models.Model):
    _name = 'ms.custormer.occupation'
    _description = 'ข้อมูลอาชีพของลูกค้า'

    name = fields.Char(string='รหัสอาชีพ', required=True)
    customer_id = fields.Many2one('ms.custormer.details', string='ลูกค้า', required=True, ondelete='cascade')
    business_type_id = fields.Char(string='ประเภทธุรกิจ')
    business_size_id = fields.Char( tring='ขนาดธุรกิจ')
    occupation_type_id = fields.Char(string='ประเภทอาชีพ')
    company = fields.Char(string='ชื่อบริษัท')
    income_type_id = fields.Char( string='ประเภทรายได้')
    employment_status_id = fields.Char( string='สถานะการทำงาน')
    start_date = fields.Date(string='วันที่เริ่ม')
    end_date = fields.Date(string='วันที่สิ้นสุด')
    duration_year = fields.Integer(string='ระยะเวลาทำงาน (ปี)')
    duration_month = fields.Integer(string='ระยะเวลาทำงาน (เดือน)')
    salary = fields.Float(string='เงินเดือน')
    overtime = fields.Float(string='เงินโอที')
    other_income = fields.Float(string='รายได้อื่นๆ')
    other_income_description = fields.Char(string='รายละเอียดรายได้อื่นๆ')
    ncb_debt = fields.Float(string='หนี้ NCB')
    other_expense = fields.Float(string='ค่าใช้จ่ายอื่นๆ')
    other_expense_description = fields.Char(string='รายละเอียดค่าใช้จ่ายอื่นๆ')
    coborrower_net_income = fields.Float(string='รายได้สุทธิของผู้ร่วมกู้')
    income_source = fields.Char(string='แหล่งที่มาของรายได้')
    income_source_type = fields.Char(string='ประเภทของแหล่งที่มาของรายได้')
    product_type = fields.Char(string='ประเภทของผลิตภัณฑ์')
    frequency_per_year = fields.Float(string='ความถี่ต่อปี')














