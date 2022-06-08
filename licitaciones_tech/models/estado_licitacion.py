from odoo import models, fields


class EstadoLicitacionAdjudicada(models.Model):
    _name = 'licitaciones_tech.estado_licitacion_adjudicada'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre de Estado')


class EstadoLicitacionEjecucion(models.Model):
    _name = 'licitaciones_tech.estado_licitacion_ejecucion'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre de Estado')