# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomizationCrm(models.Model):
    _inherit = 'crm.lead'

    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Preventas')

    def action_assign_presale(self):
        for rec in self:
            employees = rec.employee_ids.ids
            if rec.env.user.employee_id not in rec.employee_ids.ids:
                employees.append(rec.env.user.employee_id.id)
                rec.employee_ids = rec.env['hr.employee'].browse(employees)
