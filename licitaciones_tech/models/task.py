from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Task(models.Model):
    _inherit = 'project.task'

    estado_licitacion_adjudicada = fields.Many2one('licitaciones_tech.estado_licitacion_adjudicada', track_visibility='onchange')
    estado_licitacion_ejecucion = fields.Many2one('licitaciones_tech.estado_licitacion_ejecucion', track_visibility='onchange')
    es_licitacion_adjudicada = fields.Boolean(string="Es licitacion Adjudicada?",
                                              related='stage_id.subestado_licitacion_adjudicada')
    es_licitacion_ejecucion = fields.Boolean(string="Es licitacion Ejecucion?",
                                             related='stage_id.subestado_licitacion_ejecucion')
    es_perdido = fields.Boolean(string='es_perdido', compute='_actualizar_es_perdido', store=True)
    motivo_perdida_id = fields.Many2one('licitaciones_tech.motivo_perdida', track_visibility='onchange')
    es_proyecto_licitacion = fields.Boolean(related='project_id.tipo_licitacion')
    tipo_procedimiento_id = fields.Many2one('licitaciones_tech.tipo.procedimiento', track_visibility='onchange')
    modalidad_procedimiento_id = fields.Many2one('licitaciones_tech.modalidad.procedimiento',
                                                 track_visibility='onchange')
    sistema_adjudicacion = fields.Selection(
        {('lote', 'Por Lote'), ('total', 'Por el Total')}, string="Sistema de Adjudicacion")
    monto_llamado = fields.Monetary(currency_field='currency_llamado_id', string="Monto Llamado",
                                    track_visibility='onchange')
    currency_llamado_id = fields.Many2one('res.currency', string="Moneda Llamado", default=lambda self: self.env.user.company_id.currency_id,
                                  required=True, track_visibility='onchange')
    monto_adjudicado = fields.Monetary(currency_field='currency_adjudicado_id', string='Monto Adjudicado',
                                       track_visibility='onchange')
    currency_adjudicado_id = fields.Many2one('res.currency', string="Moneda Adjudicado",
                                          default=lambda self: self.env.user.company_id.currency_id,
                                        track_visibility='onchange')

    @api.onchange('monto_llamado', 'currency_llamado_id')
    def cambio_monto_llamado(self):
        if self.sistema_adjudicacion == 'total':
            self.monto_adjudicado = self.monto_llamado
        self.currency_adjudicado_id = self.currency_llamado_id

    @api.multi
    @api.depends('stage_id')
    def _actualizar_es_perdido(self):
        for rec in self:
            if rec.stage_id.es_etapa_perdida:
                if not rec.motivo_perdida_id:
                    rec.es_perdido = False
                    raise UserError('Debe ingresar un motivo de perdida. Favor pulsar el boton Marcar Perdido')
                else:
                    rec.es_perdido = True
            else:
                rec.es_perdido = False
                rec.motivo_perdida_id = None

    @api.one
    @api.constrains("monto_llamado")
    def _check_monto_llamado(self):
        if self.es_proyecto_licitacion and self.monto_llamado <= 0:
            raise ValidationError('El monto del llamado de la licitacion debe ser mayor a 0')


