# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_line_preventa_ids = fields.One2many(
        comodel_name='crm.lead.line.preventa',
        inverse_name='lead_id',
        string='Preventas'
    )

    @api.multi
    @api.constrains('lead_line_preventa_ids')
    def _constrains_lead_line_preventa_ids(self):
        for record in self:
            exist_preventa_list = []
            for line in record.lead_line_preventa_ids:
                if line.preventa_id.id in exist_preventa_list:
                    raise ValidationError(_('Preventa duplicado'))
                exist_preventa_list.append(line.preventa_id.id)

    @api.multi
    def assign_preventa_to_self(self):
        self.ensure_one()
        if self.env.user not in self.lead_line_preventa_ids.mapped('preventa_id'):
            self.lead_line_preventa_ids = [(0, 0, {'lead_id': self.id, 'preventa_id': self.env.user})]
