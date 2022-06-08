# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2.extensions import AsIs

from odoo import fields, models, tools, api


class ActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "crm.product.report"
    _auto = False
    _description = "CRM Pipeline by Product Analysis"
    _rec_name = 'id'

    lead_id = fields.Many2one('crm.lead', 'Oportunidad', readonly=True)
    active = fields.Boolean('Activo', readonly=True)
    campaign_id = fields.Many2one('utm.campaign', 'Campaña', readonly=True)
    country_id = fields.Many2one('res.country', 'Pais', readonly=True)
    company_id = fields.Many2one('res.company', 'Compañia', readonly=True)
    create_date = fields.Datetime('Fecha de Creacion', readonly=True)
    date_closed = fields.Datetime('Fecha de Cierre', readonly=True)
    date_conversion = fields.Datetime('Fecha de Conversion', readonly=True)
    date_deadline = fields.Datetime('Fecha limite', readonly=True)
    date_open = fields.Datetime('Fecha de apertura', readonly=True)
    lost_reason = fields.Many2one('crm.lost.reason', 'Motivo de Perdida',
                                  readonly=True)
    name = fields.Char('Oportunidad', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Cliente',
                                 readonly=True)
    partner_name = fields.Char('Nombre de Contacto', readonly=True)
    probability = fields.Float(group_operator='avg',
                               readonly=True, string='Probabilidad')
    stage_id = fields.Many2one('crm.stage', 'Etapa', readonly=True)
    moneda_id = fields.Many2one('res.currency', 'Moneda')
    team_id = fields.Many2one('crm.team', 'Equipo de Ventas', readonly=True)
    type = fields.Char(
        string='Tipo',
        selection=[('lead', 'Lead'), ('opportunity', 'Opportunity')],
        help="Type is used to separate Leads and Opportunities")
    user_id = fields.Many2one('res.users', 'Comercial', readonly=True)
    category_id = fields.Many2one('product.category', 'Categoria',
                                  readonly=True)
    expected_revenue = fields.Float(readonly=True, string='Ingresos esperados')
    planned_revenue = fields.Float(readonly=True, string='Ingresos previstos')
    product_id = fields.Many2one('product.product', 'Producto', readonly=True)
    product_qty = fields.Integer(readonly=True, string='Cantidad de Producto')
    product_tmpl_id = fields.Many2one('product.template', 'Plantilla de Producto',
                                      readonly=True)
    margen = fields.Float(readonly=True)
    costo_unitario = fields.Float(read_only=True)
    costo_total = fields.Float(read_only=True)
    proveedor_id = fields.Many2one('res.partner', string="Proveedor")

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
                l.company_currency as moneda_id,
                l.team_id,
                l.user_id,
                ll.category_id,
                ll.expected_revenue,
                ll.planned_revenue,
                ll.product_id,
                ll.product_qty,
                ll.product_tmpl_id,
                ll.margen,
                ll.costo_unitario,
                ll.costo_total,
                ll.proveedor_id
        """

    def _from(self):
        return """
            FROM crm_lead AS l
        """

    def _join(self):
        return """
            JOIN crm_lead_line AS ll ON l.id = ll.lead_id
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
