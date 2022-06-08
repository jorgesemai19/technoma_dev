from odoo import fields, models, api


class CrmStatus(models.Model):
    _name = 'crm.status'

    name = fields.Char(
        string='Name',
        required=False)
    percentage = fields.Float(
        string='Percentage',
        required=False)