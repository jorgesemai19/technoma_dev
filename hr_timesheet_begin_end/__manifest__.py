# Copyright 2015 Camptocamp SA - Guewen Baconnier
# Copyright 2017 Tecnativa, S.L. - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{'name': 'Timesheet Begin/End Hours',
 'version': '12.0.1.1.1',
 'author':  'Camptocamp, '
            'Tecnativa, '
            'Odoo Community Association (OCA)',
 'license': 'AGPL-3',
 'category': 'Human Resources',
 'depends': ['timesheet_grid', 'helpdesk_timesheet',
             'hr_timesheet_role', 'technoma', 'hr_timesheet_report'
             ],
 'data': ['views/hr_analytic_timesheet.xml',
          'views/helpdesk_timesheet.xml',
          'views/project_task_timesheet.xml',
          'views/menu_item_timesheet.xml',
          'views/hr_timesheets_filters.xml',
          'report/hr_timesheet_report.xml'
          ],
 'installable': True,
 'auto_install': False,
 }
