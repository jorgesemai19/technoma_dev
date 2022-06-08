from odoo import models, fields


class TipoProcedimiento(models.Model):
    _name = 'licitaciones_tech.tipo.procedimiento'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)