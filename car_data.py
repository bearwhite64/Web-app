from odoo import models, fields

class VehicleInfo(models.Model):
    _name = 'vehicle.info'
    _description = 'Vehicle Information'

    # ฟิลด์ข้อมูล
    store_name = fields.Char(string="ร้านค้า")
    category = fields.Char(string="หมวดหมู่")
    product = fields.Char(string="สินค้า")
    product_code = fields.Char(string="เลขทะเบียนสินค้า")
    brand = fields.Char(string="ยี่ห้อ")
    engine_no = fields.Char(string="เลขเครื่อง")
    chassis_no = fields.Char(string="เลขตัวถัง")
    year = fields.Char(string="ปี")
    size = fields.Float(string="ซีซี.")
    color = fields.Char(string="สี")
    sale_date = fields.Date(string="วันจำหน่ายเบื้องต้น")
    warranty_date = fields.Date(string="วันหมดประกัน")
    location = fields.Char(string="จังหวัด")
    user_name = fields.Char(string="ผู้ใช้")

