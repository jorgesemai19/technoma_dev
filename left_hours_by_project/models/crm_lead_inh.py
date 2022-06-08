from odoo import fields, models, api


class CrmLeadLeftHoursInh(models.Model):
    _inherit = 'crm.lead'

    hours_package = fields.Boolean(
        string='Is there hours package',
        required=False)
    hours_package_ids = fields.One2many(
        comodel_name='hours.package',
        inverse_name='crm_id',
        string='Hours Packages',
        required=False)
