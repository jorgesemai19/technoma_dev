# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta


class ResPartnerCustomReport(models.TransientModel):
    _name = "wizard.res.partner.custom.report"

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
            contacts = rec.env['res.partner'].search([])
            return contacts

    @api.multi
    def print_report_package_hour_xls(self):
        print('imprimir excel')
        data = {'form_data': self.get_updated_and_filter_object().ids}
        return self.env.ref('left_hours_by_project.custom_partner_report_excel').report_action(self, data=data)
