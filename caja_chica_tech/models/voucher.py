# Copyright (C) 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Voucher(models.Model):
    _inherit = 'account.voucher'
    caja_id = fields.Many2one('ruc.cajas', string="Caja Chica/Viatico", store=True)
    caja_viatico = fields.Boolean(related='payment_journal_id.caja_viatico', readonly=True)
    reposicion_caja = fields.Boolean(string='Reposicion Caja')
    diario_caja_related = fields.Many2many('ruc.cajas', compute='load_diario_caja_related')

    def get_diario_caja_related(self):
        if self.payment_journal_id and self.caja_viatico:
            diario_caja_related = (self.payment_journal_id.id,)
        else:
            diario_caja_related = self.env['account.journal'].search(['|', ('caja_chica', '=', True), ('caja_viatico',
                                                                                                       '=', True)]).ids
        domain = [('diario_caja', 'in', diario_caja_related), ('state', '=', 'abierto'), ('fondo_fijo', '=', True)]
        filtered_data = self.env['ruc.cajas'].search(domain)
        filtered_list = [x.id for x in filtered_data]
        # filtered_list = filtered_data
        return filtered_list

    @api.onchange('payment_journal_id', 'reposicion_caja')
    def onchange_payment_journal_id(self):
        res = {}
        if not self.get_diario_caja_related():
            res['domain'] = {'diario_caja_related': []}
        else:
            res['domain'] = {'diario_caja_related': [('id', '=', self.get_diario_caja_related())]}
        return res

    @api.multi
    @api.depends("payment_journal_id", "reposicion_caja")
    def load_diario_caja_related(self):
        self.diario_caja_related = [(6, 0, self.get_diario_caja_related())]

    @api.multi
    def proforma_voucher(self):
        for rec in self:
            if rec.currency_id.id != self.env.user.company_id.currency_id.id:
                fecha = rec.date
                coti = self.env['res.currency.rate'].search(
                    [['name', '=', rec.date], ['currency_id', '=', rec.currency_id.id]])
                # coti = fact.currency_id.compute(1, self.env.user.company_id.currency_id)
                if not coti:
                    raise ValidationError(
                        'No se encuentra cotizacion para el dia %s . Verifique que la cotizacion se encuentre cargada ' % fecha)
            if rec.payment_journal_id.caja_chica:
                diario_utilizado = self.env['ruc.cajas'].search(
                    [['state', '=', 'abierto'], ['diario_caja', '=', rec.payment_journal_id.id]])
                if rec.caja_id:
                    diario_utilizado = self.env['ruc.cajas'].search(
                        [['id', '=', rec.caja_id.id], ['state', '=', 'abierto'],
                         ['diario_caja', '=', rec.payment_journal_id.id]])
                if not diario_utilizado:
                    raise ValidationError(
                        'Este diario está seleccionado como Fondo Fijo, por lo que necesita una Caja abierta para poder utilizarlo. Abra una caja o utilice otro diario para realizar el pago')
                if diario_utilizado.usuario:
                    if diario_utilizado.usuario != self.env.user:
                        raise ValidationError(
                            'Solo el usuario %s, responsable de la caja puede pagar con este diario. ' % diario_utilizado.usuario.name)

                if rec.voucher_type == 'purchase' and diario_utilizado:
                    movi_obj = self.env['ruc.caja.detalle.egreso']
                    caja = diario_utilizado.id

                    factura = None
                    monto = self.amount
                    if not rec.partner_id:
                        cliente = None
                    else:
                        cliente = rec.partner_id.id
                    movi_vals = {
                        'caja_id': caja,
                        'name': rec.reference,
                        'fecha': rec.date,
                        'tipo': 'egreso',
                        'currency_id': rec.currency_id.id,
                        'monto': monto,
                        'factura': factura,
                        'cliente': cliente,
                        'pago_efectivo': self.amount,
                        'total': self.amount,
                        'voucher': self.id
                    }

                    movi_obj.create(movi_vals)
            # Si el metodo de pago no es con caja chica pero si existe una caja especificada; se trata de reposicion
            # para caja viatico
            elif rec.caja_id and rec.reposicion_caja:
                lineas = rec.line_ids
                for lin in lineas:
                    caja_chica = rec.caja_id
                    if caja_chica.state == 'abierto' and rec.voucher_type == 'purchase':
                        lineas = rec.line_ids
                        for lin in lineas:
                            caja_chica.transferencias = sum(
                                line.total for line in caja_chica.movimientos_ids) + lin.price_subtotal
                            movi_obj = self.env['ruc.caja.detalle']
                            if lin.name:
                                name = lin.name
                            elif rec.name:
                                name = rec.name
                            else:
                                name = 'Reposicion'

                            movi_vals = {
                                'caja_id': caja_chica.id,
                                'name': name,
                                'tipo': 'ingreso',
                                'voucher': rec.id,
                                'fecha': rec.date,
                                'currency_id': self.currency_id.id,
                                'monto': lin.price_subtotal,
                                'cobro_efectivo': lin.price_subtotal,
                                'total': lin.price_subtotal
                            }
                            movi_obj.create(movi_vals)
                            caja_chica.write({'saldo_inicial': caja_chica.saldo_inicial + lin.price_subtotal})
                    else:
                        diario = self.env['account.journal'].search(
                            [('default_debit_account_id', '=', lin.account_id.id), ('caja_chica', '=', True)])
                        if diario:
                            diario_utilizado = self.env['ruc.cajas'].search(
                                [['state', '=', 'abierto'], ['diario_caja', '=', diario.id]])
                            if not diario_utilizado:

                                raise ValidationError(
                                    'Está intentando cargar saldo a la cuenta %s que no posee una caja abierta. Abra la caja correspondiente y luego intente de vuelta esta operación.' % lin.account_id.name)
                            else:

                                if rec.voucher_type == 'purchase':

                                    diario_utilizado.transferencias = sum(
                                        line.total for line in diario_utilizado.movimientos_ids) + lin.price_subtotal

                                    movi_obj = self.env['ruc.caja.detalle']
                                    if lin.name:
                                        name = lin.name
                                    elif rec.name:
                                        name = rec.name
                                    else:
                                        name = 'Reposicion'

                                    movi_vals = {
                                        'caja_id': diario_utilizado.id,
                                        'name': name,
                                        'tipo': 'ingreso',
                                        'voucher': rec.id,
                                        'fecha': rec.date,
                                        'currency_id': self.currency_id.id,
                                        'monto': lin.price_subtotal,
                                        'cobro_efectivo': lin.price_subtotal,
                                        'total': lin.price_subtotal
                                    }
                                    movi_obj.create(movi_vals)
        res = super(Voucher, self).proforma_voucher()
