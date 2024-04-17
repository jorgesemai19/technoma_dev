from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class AccountAnalyticLineReportWizard(models.TransientModel):
    _name = 'account.analytic.line.report.wizard'
    _description = 'Analytic Line Report Wizard'

    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)
    all_employees = fields.Boolean(
        string='All Employees?',
        required=False)

    def print_report(self):
        work_start_time = 9.0  # Representing 9:00 AM
        work_end_time = 18.0  # Representing 6:00 PM
        domain = []
        full_employees = self.env['hr.employee'].search_read()
        if self.date_start:
            domain += [('date', '>=', self.date_start)]
        if self.date_end:
            domain += [('date', '<=', self.date_end)]
        if self.employee_id:
            domain += [('employee_id', '=', self.employee_id.id)]
        domain += ['|', ('is_used_hours', '=', True), ('overtime_hours', '!=', 0.0)]
        overtime_hours = self.env['account.analytic.line'].search_read(domain)
        data = {
            'form': self.read()[0],
            'overtime_hours': overtime_hours,
            'employees': full_employees,
        }
        return self.env.ref('customization_technoma_timesheet.overtime_report_tec').report_action(self, data=data)


