# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    project_id = fields.Many2one('project.project', string='Proyecto', track_visibility='onchange')


    @api.multi
    def generar_proyecto_oportunidad(self):
        self.ensure_one()
        if not self.project_id:
            project = self.env['project.project'].create({'name': self.display_name,
                                   'partner_id': self.partner_id.id,
                                   'user_id': self.env.uid,
                                   'lead_id': self.id})
            self.write({'project_id': project.id})
