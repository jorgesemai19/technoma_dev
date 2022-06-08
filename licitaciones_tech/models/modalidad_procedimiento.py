from odoo import models, fields, api


class ModalidadProcedimiento(models.Model):
    _name = 'licitaciones_tech.modalidad.procedimiento'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre')
