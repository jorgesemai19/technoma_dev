from odoo import models, fields


class ProjectTaskType(models.Model):
    _inherit = 'project.project'

    tipo_licitacion = fields.Boolean(string='Tipo Licitacion?', help='Marque esta casilla si la etapa es sobre ' \
                                                                    'seguimiento de licitaciones')
