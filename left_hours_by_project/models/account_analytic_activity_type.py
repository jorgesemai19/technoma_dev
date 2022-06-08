from odoo import fields, models, api
from datetime import datetime, timedelta


class ActivityType(models.Model):
    _name = 'account.analytic.activity.type'

    name = fields.Char(
        string='Name',
        required=False)