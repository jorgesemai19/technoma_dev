from odoo import fields, models, api
from datetime import datetime, timedelta


class AccountAnalyticLineInh(models.Model):
    _inherit = 'account.analytic.line'

    hours_package_id = fields.Many2one(
        comodel_name='hours.package',
        string='Hours package',
        required=False)
    extra_hours = fields.Float(
        string='Extra hours',
        compute='get_extra_hours')
    activity_type_id = fields.Many2one(
        comodel_name='account.analytic.activity.type',
        string='Activity type',
        required=False)

    @api.depends('time_start','time_stop','unit_amount')
    def get_extra_hours(self):
        for rec in self:
            i = 9
            f = 18
            day = rec.date.weekday()
            if int(day) == 5 or int(day) == 6:
                rec.extra_hours = rec.unit_amount
            else:
                if rec.time_start < i and rec.time_start != 0:
                    if (rec.time_start + rec.unit_amount) <= i:
                        rec.extra_hours = rec.unit_amount
                    else:
                        rec.extra_hours = rec.unit_amount - (rec.time_stop - i)
                else:
                    if rec.time_start >= f:
                        rec.extra_hours = rec.unit_amount
                    else:
                        if (rec.time_start + rec.unit_amount) > f:
                            rec.extra_hours = (rec.time_start + rec.unit_amount) - f
