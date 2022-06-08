# Copyright 2015 Camptocamp SA - Guewen Baconnier
# Copyright 2017 Tecnativa, S.L. - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import timedelta

from odoo import models, fields, api, exceptions, _
from odoo.tools.float_utils import float_compare


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    time_start = fields.Float(string='Begin Hour', digits=(2, 13))
    time_stop = fields.Float(string='End Hour', digits=(2, 13))
    time_type_id = fields.Many2one(string='Modalidad')
    partner_move_line = fields.Char(string="Cliente", compute='_get_partner', store=True)

    @api.depends('helpdesk_ticket_id.partner_id', 'project_id.partner_id', 'partner_id')
    def _get_partner(self):
        for rec in self:
            partner_move_line = rec.partner_id
            project_move_line = rec.project_id
            ticket_move_line = rec.helpdesk_ticket_id
            string = ''
            if partner_move_line:
                string = partner_move_line.name
            else:
                if project_move_line:
                    string = project_move_line.partner_id.name
                    if ticket_move_line:
                        print(ticket_move_line)
                        if ticket_move_line.partner_id.company_type == 'person':
                            if ticket_move_line.partner_id.parent_name:
                                string = ticket_move_line.partner_id.parent_name
                            else:
                                string = ticket_move_line.partner_id.name
                        else:
                            string = ticket_move_line.partner_id.name
            rec.partner_move_line = string

    @api.onchange('project_id')
    def onchange_project_id(self):
        partner = self.project_id.partner_id
        self.partner_id = partner
        return super().onchange_project_id()
