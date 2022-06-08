from odoo import models, api
from odoo.exceptions import ValidationError
from odoo import fields, models, exceptions, api


class Caja(models.Model):
    _inherit = 'ruc.cajas'

    @api.one
    @api.depends('movimientos_ids','egresos_ids','diario_caja','state')
    def obtener_saldo_actual(self):
        """"Se corrige metodo para que tenga en cuenta solo los asientos publicados"""
        if self.diario_caja and self.fondo_fijo:

            account_sum = 0
            if self.diario_caja.default_debit_account_id:
                if self.currency_id != self.env.user.company_id.currency_id:
                    amount_field = 'amount_currency'
                else:
                    amount_field = 'balance'
                query = """SELECT sum(%s) FROM account_move_line join 
                account_move on account_move_line.move_id = account_move.id
                WHERE account_id = %s and account_move.state = 'posted';""" % (amount_field,self.diario_caja.default_debit_account_id.id)
                self.env.cr.execute(query)
                query_results = self.env.cr.dictfetchall()
                # raise ValidationError('aaab %s' % self.currency_id)
                if query_results and query_results[0].get('sum') != None:
                    account_sum = query_results[0].get('sum')
            self.saldo_actual = account_sum


    @api.model
    def create(self, vals):

        cajas_abier = self.env['ruc.cajas'].search(
            [['state', 'in', ('borrador', 'abierto')], ['diario_caja', '=', vals.get('diario_caja')]])
        # ID DIARIO CAJA VIATICO ESPECIAL = 68
        diario_caja = self.env['account.journal'].search([('id', '=', vals['diario_caja'])])
        if cajas_abier and not diario_caja.caja_viatico:
            raise ValidationError(
                'No se puede crear una caja nueva si hay otra caja con el mismo diario en estado abierto')

        config_id = vals.get('diario_caja')
        if config_id:
            if vals.get('control_de_caja'):
                lines = self.env['account.cashbox.line'].search([('diario', '=', config_id)])

                vals['monedas_caja_ids'] = [
                    [0, 0, {'denominacion': line.coin_value, 'cantidad': line.number, 'total': line.subtotal}] for line
                    in lines]

        return super(Caja, self).create(vals)

    def abrir_caja(self):
        super(Caja, self).abrir_caja()
        if self.fondo_fijo and self.diario_caja.caja_viatico and not self.cheque_repo:
            self.saldo_inicial = 0

    @api.onchange('date', 'usuario', 'diario_caja')
    def cambiar_nombre(self):
        for caja in self:
            if caja.date:
                if self.control_de_usuario:
                    if self.usuario:
                        nombre = self.usuario.name
                else:
                    nombre = caja.diario_caja.name
                fec = caja.date
                fech = str(fec)
                name = nombre + ' - ' + fech
                caja.name = name

class AccountJournal(models.Model):
    _inherit = 'account.journal'
    caja_viatico = fields.Boolean(string="Diario para Caja Viatico?", default=False)
