from odoo import models, fields


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    proyecto_licitacion = fields.Boolean(related='project_ids.tipo_licitacion', string="Es Proyecto Licitacion?")
    subestado_licitacion_adjudicada = fields.Boolean(string="Estados Licitacion Adjudicada?", help="Marque esta casilla"
                                                                                                   "si esta etapa "
                                                                                                   "maneja subestado "
                                                                                                   "de Etapa de "
                                                                                                   "Adjudicacion")
    subestado_licitacion_ejecucion = fields.Boolean(string="Estados Licitacion en Ejecucion?",
                                                    help="Marque esta casilla"
                                                         "si esta etapa "
                                                         "maneja subestado "
                                                         "de Etapa de "
                                                         "Ejecucion")
    es_etapa_perdida = fields.Boolean(string='Etapa Perdida?', help="Marque esta casilla si esta etapa "
                                                                    "es de licitaciones perdidas")
