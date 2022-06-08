# -*- coding: utf-8 -*-
{
    'name': "Remision Technoma",

    'summary': """
        Modulo de Remisiones""",

    'description': """
        Impresion de Remision Technoma 
    """,

    'author': "Laura Gauto",


    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'remision'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/remision_report.xml',
        'views/partner.xml',
        'views/picking.xml',
    ],

}