# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployeeInh(models.Model):
    _inherit = 'hr.employee'

    # lead_id = fields.Many2one(
    #     comodel_name='crm.lead',
    #     string='Lead_id',
    #     required=False)
