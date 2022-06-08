# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class CrmLead(models.Model):
    def _get_default_modelo_tipificacion(self):
        modelos = self.env['crm.modelo.tipificacion.proyecto'].search([])
        return modelos[0] if modelos else False

    _inherit = "crm.lead"


    _sql_constraints = [
        ('check_margen', 'check(margen >= 0 and margen <= 100)',
         'El margen debe ser entre 0% y 100%!')
    ]

    @api.multi
    @api.depends('margen')
    def _compute_rentabilidad(self):
        for rec in self:
            rec.rentabilidad = 100 - rec.margen

    margen = fields.Float(default=0)
    rentabilidad = fields.Float(compute='_compute_rentabilidad', compute_sudo=True, store=True)
    valor_estrategico = fields.Many2one('crm.escala.estrategico',
                                        domain="[('modelo_tipificacion_id','=', 'modelo_tipificacion_proyecto_id')]",
                                        track_visibility='onchange')
    valor_complejidad = fields.Many2one('crm.escala.complejidad',
                                        domain="[('modelo_tipificacion_id','=', 'modelo_tipificacion_proyecto_id')]",
                                        track_visibility='onchange')
    puntos_proyecto = fields.Integer(string="Puntos de Tipo Proyecto", compute='_calcular_tipo_puntos_proyecto',
                                     readonly=True, store=True)
    tipo_proyecto = fields.Char(string="Tipo de Proyecto",  compute='_calcular_tipo_puntos_proyecto',
                                     readonly=True, store=True)
    modelo_tipificacion_proyecto_id = fields.Many2one('crm.modelo.tipificacion.proyecto',
                                                      default=_get_default_modelo_tipificacion)
    stage_name = fields.Char(related='stage_id.name')

    @api.depends('stage_id', 'valor_estrategico', 'valor_complejidad', 'margen', 'planned_revenue')
    def _calcular_tipo_puntos_proyecto(self):
        # if self.won_status == 'won':
        puntos_facturacion = self.modelo_tipificacion_proyecto_id.obtener_puntos_facturacion(self.planned_revenue)
        puntos_rentabilidad = self.modelo_tipificacion_proyecto_id.obtener_puntos_rentabilidad(self.rentabilidad)
        puntos_complejidad = self.modelo_tipificacion_proyecto_id.obtener_puntos_complejidad(self.valor_complejidad)
        puntos_estrategico = self.modelo_tipificacion_proyecto_id.obtener_puntos_estrategico(self.valor_estrategico)
        valor_rentabilidad_facturacion = self.planned_revenue * self.rentabilidad / 100
        puntos_rentabilidad_proporcional = self.modelo_tipificacion_proyecto_id. \
            obtener_puntos_rentabilidad_proporcional(valor_rentabilidad_facturacion)
        puntos_proyecto, tipo_proyecto = self.modelo_tipificacion_proyecto_id.obtener_puntos_tipo_proyecto(
            puntos_facturacion, puntos_rentabilidad, puntos_complejidad, puntos_estrategico,
            puntos_rentabilidad_proporcional)
        self.tipo_proyecto = tipo_proyecto
        self.puntos_proyecto = puntos_proyecto

    def calcular_puntos_facturacion(self):
        puntos = self.modelo_tipificacion_proyecto_id.obtener_puntos_facturacion(self.planned_revenue)
        return puntos

    def calcular_puntos_rentabilidad(self):
        puntos = self.modelo_tipificacion_proyecto_id.obtener_puntos_rentabilidad(self.rentabilidad)
        return puntos

    def calcular_puntos_complejidad(self):
        puntos = self.modelo_tipificacion_proyecto_id.obtener_puntos_complejidad(self.valor_complejidad)
        return puntos

    def calcular_puntos_estrategico(self):
        puntos = self.modelo_tipificacion_proyecto_id.obtener_puntos_estrategico(self.valor_estrategico)
        return puntos
