# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta


class UpdateAllRecordTransientModel(models.TransientModel):
    _name = "wizard.report.package.hours"

    date_from = fields.Date(
        string='Date from',
        required=True,
        default=time.strftime('%Y-%m-01'))
    date_to = fields.Date(
        string='Date_to',
        required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('approved', 'Approved'),
                   ('cancel', 'Cancel'),
                   ('consumed', 'Consumed'),
                   ('all', 'All')],
        default='all',
        required=1)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=False)
    integer_hours = fields.Boolean(
        string='Just Integer hours',
        required=False)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False,
        index=True,
        default=lambda self: self.env.user.company_id.id)

    def print_report_package_hour(self):
        self.ensure_one()
        self.sent = True
        return self.env.ref('left_hours_by_project.package_hour_report_button').report_action(self)

    @api.multi
    def get_updated_and_filter_object(self):
        for rec in self:
            packages = rec.env['hours.package'].search([])
            for p in packages:
                p.get_hours_used_and_available()
            domain = [('approval_date', '>=', rec.date_from)]
            domain += [('approval_date', '<=', rec.date_to)]
            if rec.state != 'all':
                domain += [('state', '=', rec.state)]
            if rec.partner_id:
                domain += [('partner_id', '=', rec.partner_id.id)]
            if rec.integer_hours:
                domain += (['integer_hours', '=', True])
            packages = rec.env['hours.package'].search(domain)
            return packages

    @api.multi
    def print_report_package_hour_xls(self):
        print('imprimir excel')
        data = {'form_data': self.get_updated_and_filter_object().ids,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'state': self.state,
                'partner_id': self.partner_id.id,
                'integer_hours': self.integer_hours,
                }
        print(data)
        return self.env.ref('left_hours_by_project.report_hours_package_excel').report_action(self, data=data)
