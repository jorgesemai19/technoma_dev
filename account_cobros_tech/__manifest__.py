# -*- coding: utf-8 -*-
{
    'name': "account_cobros_tech",

    'summary': """
        Modulo a medida de Recibo de Cobranzas""",

    'description': """
        Modulo a medida de Recibo de Cobranzas
    """,

    'author': "Laura Gauto",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_cobros_py'],

    # always loaded
    'data': [
        'reports/config_reports_recibo_py.xml',
        'reports/report_recibo_py.xml',
        'reports/recibo_report.xml',
        'data/recibo_sequence.xml',
        'views/recibo_view.xml',
        'data/mail_data.xml',
        'views/mail_template.xml',
    ],

}
