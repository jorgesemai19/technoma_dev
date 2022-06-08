from odoo import models, fields, api


class MotivoPerdida(models.Model):
    _name = 'licitaciones_tech.motivo_perdida'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre')
