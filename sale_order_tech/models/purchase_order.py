# -*- coding: utf-8 -*-


from odoo import api, models, fields, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    linked_origin = fields.Many2one(
        comodel_name='sale.order',
        string='Linked origin',
        required=False)