# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
import re
import math


class ModeloTipificacionProyecto(models.Model):
    _name = "crm.modelo.tipificacion.proyecto"
    _description = "Modelo Tipificacion Proyecto"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    nombre = fields.Char(string='Nombre', required=True, track_visibility='onchange')
    escalas_facturacion = fields.One2many('crm.escala.facturacion', 'modelo_tipificacion_id',
                                          string='Escalas de Facturacion')
    escalas_rentabilidad = fields.One2many('crm.escala.rentabilidad', 'modelo_tipificacion_id',
                                           string='Escalas de Rentabilidad')
    escalas_complejidad = fields.One2many('crm.escala.complejidad', 'modelo_tipificacion_id',
                                          string='Escalas de Complejidad')
    escalas_estrategico = fields.One2many('crm.escala.estrategico', 'modelo_tipificacion_id',
                                          string='Escalas de Estrategico')
    escalas_tipo_proyecto = fields.One2many('crm.escala.tipo.proyecto', 'modelo_tipificacion_id',
                                            string='Escalas de Tipo de Proyecto')
    codigo_facturacion = fields.Char(string='Codigo Facturacion', track_visibility='onchange')
    codigo_rentabilidad = fields.Char(string='Codigo Rentabilidad', track_visibility='onchange')
    codigo_complejidad = fields.Char(string='Codigo Complejidad', track_visibility='onchange')
    codigo_estrategico = fields.Char(string='Codigo Estrategico', track_visibility='onchange')
    formula = fields.Char(string='Formula Tipificacion', track_visibility='onchange')
    rentabilidad_anual = fields.Integer(string='Rentabilidad Anual', track_visibility='onchange')
    codigo_rentabilidad_proporcional = fields.Char('Codigo Rentabilidad Proporcional',
                                                   help='Los puntos de esta variable se calcula de la siguiente manera:'
                                                        'redondear([valor de rentabilidad proyecto]/[valor de '
                                                        'rentabilidad anual]',
                                                   track_visibility='onchange')

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            nombre = u"{}".format(rec.nombre)
            res.append((rec.id, nombre))
        return res

    def obtener_puntos_facturacion(self, planned_revenue):
        puntos_facturacion = 0
        for escala_facturacion in self.escalas_facturacion:
            if escala_facturacion.valor_minimo >= 0 and escala_facturacion.valor_maximo > 0:
                if planned_revenue in range(escala_facturacion.valor_minimo, escala_facturacion.valor_maximo + 1):
                    puntos_facturacion = escala_facturacion.puntos
                    break
            elif escala_facturacion.valor_maximo == 0:
                if planned_revenue >= escala_facturacion.valor_minimo:
                    puntos_facturacion = escala_facturacion.puntos
                    break
        return puntos_facturacion

    def obtener_puntos_rentabilidad(self, rentabilidad):
        puntos_rentabilidad = 0
        for escala_rentabilidad in self.escalas_rentabilidad:
            if escala_rentabilidad.valor_minimo >= 0 and escala_rentabilidad.valor_maximo > 0:
                if rentabilidad in range(escala_rentabilidad.valor_minimo, escala_rentabilidad.valor_maximo + 1):
                    puntos_rentabilidad = escala_rentabilidad.puntos
                    break
            elif escala_rentabilidad.valor_maximo == 0:
                if rentabilidad > escala_rentabilidad.valor_minimo:
                    puntos_rentabilidad = escala_rentabilidad.puntos
                    break
        return puntos_rentabilidad

    def obtener_puntos_complejidad(self, complejidad):
        puntos_complejidad = 0
        for escala_complejidad in self.escalas_complejidad:
            if complejidad == escala_complejidad:
                puntos_complejidad = escala_complejidad.puntos
                break
        return puntos_complejidad

    def obtener_puntos_estrategico(self, estrategico):
        puntos_estrategico = 0
        for escala_estrategico in self.escalas_estrategico:
            if estrategico == escala_estrategico:
                puntos_estrategico = escala_estrategico.puntos
                break
        return puntos_estrategico

    def obtener_puntos_rentabilidad_proporcional(self, rentabilidad_facturacion):
        rentabilidad_proporcional = rentabilidad_facturacion / self.rentabilidad_anual * 100
        puntos_rentabilidad_proporcional = math.ceil(rentabilidad_proporcional)
        return puntos_rentabilidad_proporcional

    def obtener_puntos_tipo_proyecto(self, puntos_facturacion, puntos_rentabilidad, puntos_complejidad,
                                     puntos_estrategico, puntos_rentabilidad_proporcional):
        formula = re.findall('[A-Z]+|.', self.formula)
        formula_valores = ''
        for i, term in enumerate(formula):
            if term == self.codigo_facturacion:
                formula_valores += str(puntos_facturacion)
            elif term == self.codigo_rentabilidad:
                formula_valores += str(puntos_rentabilidad)
            elif term == self.codigo_estrategico:
                formula_valores += str(puntos_estrategico)
            elif term == self.codigo_complejidad:
                formula_valores += str(puntos_complejidad)
            elif term == self.codigo_rentabilidad_proporcional:
                formula_valores += str(puntos_rentabilidad_proporcional)
            else:
                formula_valores += term
        puntos_total = eval(formula_valores) if formula_valores != '' else 0
        tipo_proyecto = self.obtener_tipo_proyecto(puntos_total)
        return puntos_total, tipo_proyecto

    def obtener_tipo_proyecto(self, puntos_total):
        tipo_proyecto = ''
        for escala_tipo_proyecto in self.escalas_tipo_proyecto:
            if escala_tipo_proyecto.valor_minimo >= 0 and escala_tipo_proyecto.valor_maximo > 0:
                if puntos_total in range(escala_tipo_proyecto.valor_minimo, escala_tipo_proyecto.valor_maximo + 1):
                    tipo_proyecto = escala_tipo_proyecto.nombre
                    break
            elif escala_tipo_proyecto.valor_maximo == 0:
                if puntos_total >= escala_tipo_proyecto.valor_minimo:
                    tipo_proyecto = escala_tipo_proyecto.nombre
                    break
        return tipo_proyecto


class EscalaFacturacion(models.Model):
    _name = "crm.escala.facturacion"
    _description = "Escala de Facturacion"

    nombre = fields.Char(string='Nombre', required=True, track_visibility='onchange')
    valor_minimo = fields.Integer(string='Valor minimo')
    valor_maximo = fields.Integer(string='Valor maximo')
    puntos = fields.Char(string='Puntos')
    modelo_tipificacion_id = fields.Many2one('crm.modelo.tipificacion.proyecto', string='Modelo Tipificacion Proyecto',
                                             ondelete='cascade')

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            nombre = u"{}".format(rec.nombre)
            res.append((rec.id, nombre))
        return res


class EscalaRentabilidad(models.Model):
    _name = "crm.escala.rentabilidad"
    _description = "Escala de Rentabilidad"

    nombre = fields.Char(string='Nombre', required=True, track_visibility='onchange')
    valor_minimo = fields.Integer(string='Valor minimo')
    valor_maximo = fields.Integer(string='Valor maximo')
    puntos = fields.Char(string='Puntos')
    modelo_tipificacion_id = fields.Many2one('crm.modelo.tipificacion.proyecto', string='Modelo Tipificacion Proyecto',
                                             ondelete='cascade')

    _sql_constraints = [
        ('check_valor_minimo', 'check(valor_minimo >= 0 and valor_minimo <= 100)',
         'El valor minimo debe ser entre 0% y 100%!'),
        ('check_valor_maximo', 'check(valor_maximo >= 0 and valor_maximo <= 100)',
         'El valor maximo debe ser entre 0% y 100%!')
    ]

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            nombre = u"{}".format(rec.nombre)
            res.append((rec.id, nombre))
        return res


class EscalaComplejidad(models.Model):
    _name = "crm.escala.complejidad"
    _description = "Escala de Rentabilidad"

    nombre = fields.Char(string='Nombre', required=True, track_visibility='onchange')
    puntos = fields.Char(string='Puntos')
    modelo_tipificacion_id = fields.Many2one('crm.modelo.tipificacion.proyecto', string='Modelo Tipificacion Proyecto',
                                             ondelete='cascade')

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            nombre = u"{}".format(rec.nombre)
            res.append((rec.id, nombre))
        return res


class EscalaEstrategico(models.Model):
    _name = "crm.escala.estrategico"
    _description = "Escala de Estrategico"

    nombre = fields.Char(string='Nombre', required=True, track_visibility='onchange')
    puntos = fields.Char(string='Puntos')
    modelo_tipificacion_id = fields.Many2one('crm.modelo.tipificacion.proyecto', string='Modelo Tipificacion Proyecto',
                                             ondelete='cascade')

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            nombre = u"{}".format(rec.nombre)
            res.append((rec.id, nombre))
        return res


class EscalaTipoProyecto(models.Model):
    _name = "crm.escala.tipo.proyecto"
    _description = "Escala de Tipificacion de Proyecto"

    nombre = fields.Char(string='Nombre', required=True, track_visibility='onchange')
    valor_minimo = fields.Integer(string='Valor minimo')
    valor_maximo = fields.Integer(string='Valor maximo')
    puntos = fields.Char(string='Puntos')
    modelo_tipificacion_id = fields.Many2one('crm.modelo.tipificacion.proyecto', string='Modelo Tipificacion Proyecto',
                                             ondelete='cascade')

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = u"{}".format(rec.name)
            res.append((rec.id, name))
        return res
