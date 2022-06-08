# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    code = fields.Char(
        string='Lead Number', required=True, default="/", readonly=True)
    custom_status_id = fields.Many2one(
        comodel_name='crm.status',
        string='Status',
        required=False)

    _sql_constraints = [
        ('crm_lead_unique_code', 'UNIQUE (code)',
         _('The code must be unique!')),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', '/') == '/':
                vals['code'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return super(CrmLead, self).create(vals_list)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return super(CrmLead, self).copy(default)

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = u"{} ({})".format(rec.code, rec.name)
            res.append((rec.id, name))
        return res

    # @api.model
    # def _get_default_moneda(self):
    #     moneda = self.env['res.currency'].search([('name', 'ilike', 'USD'), ('ambito', '=', 'venta')], limit=1).id
    #     return moneda
