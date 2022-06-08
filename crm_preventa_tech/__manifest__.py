# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Lead Line Preventa',
    'version': '12.0.1.0.0',
    'category': 'Customer Relationship Management',
    'license': 'LGPL-3',
    'summary': 'Adds a lead line Preventa in the lead/opportunity model '
               'in odoo',
    'author': "Laura Gauto",
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_lead_line_preventa_views.xml',
        'report/crm_preventa_report_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
