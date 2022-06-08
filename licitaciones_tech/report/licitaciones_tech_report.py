# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

# from psycopg2.extensions import AsIs
#
# from odoo import fields, models, tools, api
#
#
# class LicitacionesReport(models.Model):
#     """ Analisis de Licitaciones """
#
#     _name = "licitaciones_tech.report"
#     _auto = False
#     _description = "Analisis de Licitaciones"
#     _rec_name = 'id'
#
#     task_id = fields.Many2one('project.task', 'Licitacion', readonly=True)
#     project_id = fields.Many2one('project.project', 'Proyecto', readonly=True)
#     active = fields.Boolean('Activo', readonly=True)
#     create_date = fields.Datetime('Creado el', readonly=True)
#     date_deadline = fields.Date('Fecha limite', readonly=True)
#     estado_licitacion_adjudicada = fields.Many2one('licitaciones_tech.estado_licitacion_adjudicada',
#                                                    readonly=True)
#     estado_licitacion_ejecucion = fields.Many2one('licitaciones_tech.estado_licitacion_ejecucion',
#                                                   track_visibility='onchange')
#     es_licitacion_adjudicada = fields.Boolean(string="Es licitacion Adjudicada?",
#                                               related='stage_id.subestado_licitacion_adjudicada')
#     es_licitacion_ejecucion = fields.Boolean(string="Es licitacion Ejecucion?",
#                                              related='stage_id.subestado_licitacion_ejecucion')
#     es_perdido = fields.Boolean(string='es_perdido', compute='_actualizar_es_perdido', store=True)
#     motivo_perdida_id = fields.Many2one('licitaciones_tech.motivo_perdida', track_visibility='onchange')
#     es_proyecto_licitacion = fields.Boolean(related='project_id.tipo_licitacion')
#     tipo_procedimiento_id = fields.Many2one('licitaciones_tech.tipo.procedimiento', track_visibility='onchange')
#     modalidad_procedimiento_id = fields.Many2one('licitaciones_tech.modalidad.procedimiento',
#                                                  track_visibility='onchange')
#     sistema_adjudicacion = fields.Selection(
#         {('lote', 'Por Lote'), ('total', 'Por el Total')}, string="Sistema de Adjudicacion")
#     monto_llamado = fields.Monetary(currency_field='currency_llamado_id', string="Monto Llamado",
#                                     track_visibility='onchange')
#     currency_llamado_id = fields.Many2one('res.currency', string="Moneda Llamado",
#                                           default=lambda self: self.env.user.company_id.currency_id,
#                                           required=True, track_visibility='onchange')
#     monto_adjudicado = fields.Monetary(currency_field='currency_adjudicado_id', string='Monto Adjudicado',
#                                        track_visibility='onchange')
#     currency_adjudicado_id = fields.Many2one('res.currency', string="Moneda Adjudicado",
#                                              default=lambda self: self.env.user.company_id.currency_id,
#                                              track_visibility='onchange')
#
#
#
#
#     lost_reason = fields.Many2one('crm.lost.reason', 'Lost Reason',
#                                   readonly=True)
#     name = fields.Char('Lead Name', readonly=True)
#     partner_id = fields.Many2one('res.partner', 'Partner/Customer',
#                                  readonly=True)
#     partner_name = fields.Char('Contact Name', readonly=True)
#     probability = fields.Float('Probability', group_operator='avg',
#                                readonly=True)
#     stage_id = fields.Many2one('crm.stage', 'Stage', readonly=True)
#     team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
#     type = fields.Char(
#         string='Type',
#         selection=[('lead', 'Lead'), ('opportunity', 'Opportunity')],
#         help="Type is used to separate Leads and Opportunities")
#     user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
#     planned_revenue = fields.Float('Planned Revenue', readonly=True)
#     preventa_id = fields.Many2one('res.users', 'Preventa', readonly=True)
#
#
#     def _select(self):
#         return """
#             SELECT
#                 ROW_NUMBER() OVER (ORDER BY l.id) AS id,
#                 l.active,
#                 l.id as lead_id,
#                 l.campaign_id,
#                 l.country_id,
#                 l.company_id,
#                 l.create_date,
#                 l.date_closed,
#                 l.date_conversion,
#                 l.date_deadline,
#                 l.date_open,
#                 l.lost_reason,
#                 l.name,
#                 l.partner_id,
#                 l.partner_name,
#                 l.probability,
#                 l.type,
#                 l.stage_id,
#                 l.team_id,
#                 l.user_id,
#                 l.planned_revenue,
#                 lp.preventa_id
#         """
#
#     def _from(self):
#         return """
#             FROM crm_lead AS l
#         """
#
#     def _join(self):
#         return """
#             FULL JOIN crm_lead_line_preventa AS lp
#             ON l.id = lp.lead_id
#         """
#
#     @api.model_cr
#     def init(self):
#         tools.drop_view_if_exists(self._cr, self._table)
#         self._cr.execute("""
#             CREATE OR REPLACE VIEW %s AS (
#                 %s
#                 %s
#                 %s
#             )
#         """, (AsIs(self._table), AsIs(self._select()),
#               AsIs(self._from()), AsIs(self._join()))
#         )
