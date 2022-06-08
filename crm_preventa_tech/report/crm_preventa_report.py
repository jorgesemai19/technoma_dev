# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2.extensions import AsIs

from odoo import fields, models, tools, api


class ActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "crm.preventa.report"
    _auto = False
    _description = "CRM Pipeline by Preventa Analysis"
    _rec_name = 'id'

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    active = fields.Boolean('Active', readonly=True)
    campaign_id = fields.Many2one('utm.campaign', 'Campaing', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    create_date = fields.Datetime('Create Date', readonly=True)
    date_closed = fields.Datetime('Closed Date', readonly=True)
    date_conversion = fields.Datetime('Conversion Date', readonly=True)
    date_deadline = fields.Date('Deadline Date', readonly=True)
    date_open = fields.Datetime('Open Date', readonly=True)
    lost_reason = fields.Many2one('crm.lost.reason', 'Lost Reason',
                                  readonly=True)
    name = fields.Char('Lead Name', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner/Customer',
                                 readonly=True)
    partner_name = fields.Char('Contact Name', readonly=True)
    probability = fields.Float('Probability', group_operator='avg',
                               readonly=True)
    stage_id = fields.Many2one('crm.stage', 'Stage', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    type = fields.Char(
        string='Type',
        selection=[('lead', 'Lead'), ('opportunity', 'Opportunity')],
        help="Type is used to separate Leads and Opportunities")
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    planned_revenue = fields.Float('Planned Revenue', readonly=True)
    preventa_id = fields.Many2one('res.users', 'Preventa', readonly=True)


    def _select(self):
        return """
            SELECT
                ROW_NUMBER() OVER (ORDER BY l.id) AS id,
                l.active,
                l.id as lead_id,
                l.campaign_id,
                l.country_id,
                l.company_id,
                l.create_date,
                l.date_closed,
                l.date_conversion,
                l.date_deadline,
                l.date_open,
                l.lost_reason,
                l.name,
                l.partner_id,
                l.partner_name,
                l.probability,
                l.type,
                l.stage_id,
                l.team_id,
                l.user_id,
                l.planned_revenue,
                lp.preventa_id
        """

    def _from(self):
        return """
            FROM crm_lead AS l
        """

    def _join(self):
        return """
            FULL JOIN crm_lead_line_preventa AS lp
            ON l.id = lp.lead_id
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """, (AsIs(self._table), AsIs(self._select()),
              AsIs(self._from()), AsIs(self._join()))
        )
