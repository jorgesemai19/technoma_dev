from odoo import api, fields, models, _


class SaleOrder(models.Model):

    _inherit = "sale.order"
    tipo_proyecto = fields.Char(related='opportunity_id.tipo_proyecto', store=True, string="Tipo Proyecto")