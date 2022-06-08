# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLeadLine(models.Model):
    _name = "crm.lead.line.preventa"
    _description = "Lineas de Preventa en Oportunidad"
    lead_id = fields.Many2one('crm.lead', string='Lead')
    preventa_id = fields.Many2one("res.users", 'Preventa', required=True, translate=True)

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = rec.preventa_id.name
            res.append((rec.id, name))
        return res
