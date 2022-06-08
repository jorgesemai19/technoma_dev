# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta


class WizardReportExtraHours(models.TransientModel):
    _name = "wizard.report.extra.hours"

    date_from = fields.Date(
        string='Date from',
        required=True,
        default=time.strftime('%Y-%m-01'))
    date_to = fields.Date(
        string='Date_to',
        required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False,
        index=True,
        default=lambda self: self.env.user.company_id.id)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)
    detailed = fields.Boolean(
        string='Detailed?',
        required=False)

    def print_report_extra_hours(self):
        self.ensure_one()
        self.sent = True
        return self.env.ref('left_hours_by_project.extra_hour_report_button').report_action(self)

    def get_object_lines(self):
        if self.employee_id:
            lines = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        else:
            lines = self.env['hr.employee'].search([])
        return lines

    def get_detail_lines(self, employee):
        details_object = self.env['account.analytic.line'].search([('employee_id', '=', employee.id),
                                                                   ('date', '>=', self.date_from),
                                                                   ('date', '<=', self.date_to)]).sorted(key=lambda r: r.date)
        print(details_object)
        return details_object

    def get_total_extra_hours(self, employee, date_from, date_to):
        t_object = self.env['account.analytic.line'].search([('employee_id', '=', employee.id),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to)])
        total_extra_hours = sum([line.extra_hours for line in t_object])
        return total_extra_hours

    @api.multi
    def print_report_extra_hour_xls(self):
        print('imprimir excel')
        # data = {'form_data': self.get_updated_and_filter_object().ids,
        #         'date_from': self.date_from,
        #         'date_to': self.date_to,
        #         'state': self.state,
        #         'partner_id': self.partner_id.id,
        #         'integer_hours': self.integer_hours,
        #         }
        # print(data)
        # return self.env.ref('left_hours_by_project.report_hours_package_excel').report_action(self, data=data)
