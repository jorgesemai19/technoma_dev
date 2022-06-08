# -*- coding: utf-8 -*-
{
    'name': "left_hours_by_project",

    'summary': """
        Have control about your hours package 
        """,

    'description': """
        This module handles the hours package crated in the CRM module to have control about 
        the hours consumed in timesheet in relation to budget
    """,

    'author': "Technoma",
    'website': "http://www.technoma.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','hr_timesheet','sale', 'project', 'helpdesk'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
        'report/extra_hours_report_template.xml',
        'views/crm_lead_inh_view_lh.xml',
        'views/hours_package_views.xml',
        'views/account_analytic_view_inh.xml',
        'views/project_task_view_inh.xml',
        'views/helpdesk_ticket_view_inh.xml',
        'data/package_hours_cron.xml',
        'wizard/wizard_update_all_package_hours_view.xml',
        'report/hour_package_reports.xml',
        'report/hours_package_template.xml',
        'report/hours_package_detail.xml',
        'wizard/wizard_report_hours_package.xml',
        'wizard/wizard_report_extra_hours.xml',
        'views/hours_package_menu.xml',
        'wizard/wizard_res_partner_custom_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}