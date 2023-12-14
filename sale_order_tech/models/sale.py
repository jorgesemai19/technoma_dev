# -*- coding: utf-8 -*-

import re

from odoo import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    monto_margen = fields.Monetary(string='Monto Margen', track_visibility='onchange')
    porcentaje_margen = fields.Float(track_visibility='onchange')
    linked_po = fields.Many2one(
        comodel_name='purchase.order',
        string='Linked purchase order',
        required=False)

    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()
        po = self.env['purchase.order'].search([('origin', '=like', self.name)])
        if po:
            po[0].linked_origin = self.id
            self.linked_po = po[0].id
        return result