from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    caja_id = fields.Many2one('ruc.cajas')
    caja_viatico = fields.Boolean(related='journal_id.caja_viatico', readonly=True)

    @api.multi
    def post(self):
        for rec in self:
            if rec.caja_id:
                diario_utilizado = self.env['ruc.cajas'].search(
                    [['id', '=', rec.caja_id.id], ['state', '=', 'abierto']])
            else:
                if rec.journal_id.caja_chica:
                    diario_utilizado = self.env['ruc.cajas'].search(
                        [['state', '=', 'abierto'], ['diario_caja', '=', rec.journal_id.id]])
            if not diario_utilizado:
                raise ValidationError(
                    'Este diario está seleccionado como Fondo Fijo, por lo que necesita una Caja abierta para poder utilizarlo. Abra una caja o utilice otro diario para realizar el pago')
            if diario_utilizado.usuario:
                if diario_utilizado.usuario != self.env.user:
                    raise ValidationError(
                        'Solo el usuario %s, responsable de la caja puede pagar con este diario. ' % diario_utilizado.usuario.name)
            if rec.payment_type == 'outbound' and diario_utilizado:
                movi_obj = self.env['ruc.caja.detalle.egreso']
                caja = diario_utilizado.id

                # if rec.fac_ids:
                #     descripcion = 'Pago de Factura Nro. ' + str(self.fac_ids.nro_factura)
                # else:
                #    descripcion = self.motivo
                if len(rec.invoice_ids) > 1:
                    for faaa in rec.invoice_ids:
                        movi_vals = {
                            'caja_id': caja,
                            'name': rec.communication,
                            'fecha': rec.payment_date,
                            'tipo': 'egreso',
                            'currency_id': faaa.currency_id.id,
                            'monto': faaa.amount_total,
                            'factura': faaa.id,
                            'cliente': faaa.partner_id.id,
                            'pago_efectivo': faaa.amount_total,
                            'total': faaa.amount_total,
                            'pago': self.id
                        }

                        movi_obj.create(movi_vals)
                else:
                    if not rec.invoice_ids:
                        factura = None
                        monto = self.amount
                    else:
                        for fac in rec.invoice_ids:
                            factura = fac.id
                            monto = rec.invoice_ids.amount_total
                    if not rec.partner_id:
                        cliente = None
                    else:
                        cliente = rec.partner_id.id
                    movi_vals = {
                        'caja_id': caja,
                        'name': rec.communication,
                        'fecha': rec.payment_date,
                        'tipo': 'egreso',
                        'currency_id': rec.currency_id.id,
                        'monto': monto,
                        'factura': factura,
                        'cliente': cliente,
                        'pago_efectivo': rec.amount,
                        'total': rec.amount,
                        'pago': rec.id
                    }

                    movi_obj.create(movi_vals)

        res = super(AccountPayment, self).post()
        return res
