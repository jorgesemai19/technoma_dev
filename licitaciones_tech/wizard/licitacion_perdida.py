# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LicitacionPerdida(models.TransientModel):
    _name = 'licitaciones_tech.licitacion.perdida'
    _description = 'Motivo de Perdida'

    motivo_perdida_id = fields.Many2one('licitaciones_tech.motivo_perdida', 'Motivo de Perdida')

    @api.multi
    def action_aplicar_motivo_perdida(self):
        licitaciones = self.env['project.task'].browse(self.env.context.get('active_ids'))

        etapa_perdido = licitaciones.project_id.type_ids.filtered(lambda x: x.es_etapa_perdida == True)

        licitaciones.write({'motivo_perdida_id': self.motivo_perdida_id.id, 'es_perdido': True,
                            'stage_id': etapa_perdido.id})
