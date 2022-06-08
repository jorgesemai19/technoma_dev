from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'hours.package.type'

    name = fields.Char(string='Description')
