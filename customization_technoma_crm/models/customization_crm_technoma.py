# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomizationCrm(models.Model):
    _inherit = 'crm.lead'

    presales_id = fields.Many2one(
        comodel_name='res.users',
        string='Presales',
        required=False)

    def action_assign_presale(self):
        self.ensure_one()
        self.presales_id = self.env.user