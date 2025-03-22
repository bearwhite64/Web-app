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

{
    "name": "Update Sale",
    'version': '16.0.1.0.0',
    "summary": """Update Sale""",
    "description": """Provide Sale""",
    "category": "Sales",
    'author': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    "depends": ['sale'],
    "data": ['views/sale_order_view.xml',
            'views/purchase_order_view.xml',
            'security/ir.model.access.csv',
             # 'views/menu_master_view.xml',
             # 'views/new_account_move_line.xml',
             'views/print_report.xml',
             'views/contact_view.xml',
             'views/payment_view.xml',
             'views/collector_view.xml',
             'views/transfer_work_view.xml',
             'views/assign_work_view.xml',
             'views/create_data_view.xml',
             'views/job_transfer_report_view.xml',
             'views/contact_detail.xml',
             # 'views/contract_record_views.xml',
             'views/partner_view.xml',
             'views/calculate_penalty.xml',
             'views/notice_view.xml',
             'views/assign_approve_view.xml',
             'views/report_account_view.xml',
             'views/report_performance_view.xml',
             'views/transfer_approve.xml',
             # 'views/contact_history_views.xml',
             'views/contact_record_views.xml',
             'views/vehicle_info_view.xml',





             ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
