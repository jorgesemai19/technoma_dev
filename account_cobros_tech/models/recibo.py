from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Recibo(models.Model):
    _inherit = 'account.recibo'
    name = fields.Char(string='Recibo Nro', readonly=True, copy=False)

    def agregar_punto_de_miles(self, numero, moneda):
        if 'USD' in moneda.name:
            entero = int(numero)
            decimal = '{0:.2f}'.format(numero - entero)
            entero_string = '.'.join([str(int(entero))[::-1][i:i + 3] for i in range(0, len(str(int(entero))), 3)])[
                            ::-1]
            if decimal == '0.00':
                numero_con_punto = entero_string
            else:
                decimal_string = str(decimal).split('.')
                numero_con_punto = entero_string + ',' + decimal_string[1]
        else:
            numero_con_punto = '.'.join([str(int(numero))[::-1][i:i + 3] for i in range(0, len(str(int(numero))), 3)])[
                               ::-1]
        return numero_con_punto

    def sacasimbolo_(self, a):
        b = str(a)
        c = b.split(" ")

        return c[0]

    def cambiapuntoporcoma(self, a):
        b = str(a)
        c = b.replace(".", ",")

    def agregar_punto_de_miles_(self, numero):
        numero_con_punto = '.'.join([str(int(numero))[::-1][i:i + 3] for i in range(0, len(str(int(numero))), 3)])[::-1]
        return numero_con_punto

    def puntodemiles(self, a):
        b = str(a)
        c = b.split(',')
        if len(c) > 1:
            d = self.agregar_punto_de_miles_(c[0])
            e = str(d) + ',' + str(c[1])
            return e
        else:
            return b

    @api.multi
    def set_confirmado(self):
        if self.state != 'confirmado':
            #             self.set_amount_gs()
            if not self.name:
                self.name = self.env['ir.sequence'].get('account.cobros.recibo')
            if self.payment_ids:
                # DONDE SE APLICA LA RETENCION A LAS FACTURAS CON MAYOR MONTOS PRIMERAMENTE
                nc = self.pagos_facturas_ids.filtered(
                    lambda r: r.invoice_id.residual > 0 and r.invoice_id.type in ('out_refund', 'in_refund'))
                if nc:
                    for nota in nc:
                        # SI EN EL CASO LA NOTA DE CREDITO QUEDA CON SALDO QUE APLIQUE A LAS SIGUIENTE FACTURA
                        while (nota.invoice_id.residual > 0):
                            for fac in self.pagos_facturas_ids.filtered(
                                    lambda r: r.amount > 0 and r.invoice_id.type == 'out_invoice').sorted(
                                key=lambda r: r.amount, reverse=True):
                                # if fac.amount == fac.invoice_id.residual:
                                # BUSCAMOS EL REGISTRO DE LA NOTA DE CREDITO YA QUE SOLO TENEMOS EL ID QUE ESTA DENTRO DE NOTAS
                                nota_de_credito = self.env['account.invoice'].search(
                                    [['id', '=', nota.invoice_id.id]])
                                # VERIFICAMOS IS LA NOTA DE CREDITO TIENE SALDO MAYOR A 0
                                if nota_de_credito.residual > 0:
                                    # SI LA NOTA DE CREDITO TIENE SALDO MAYOR A 0 BUSCAMOS LA LINEA DE ASIENTO QUE CORRESPONDE A ESA NOTA DE CREDITO
                                    nota_credito_line = self.env['account.move.line'].search(
                                        [['invoice_id', '=', nota.invoice_id.id], ['user_type_id', '=', 1]])

                                    # ASIGNAMOS EL VALOR DEL SALDO DE LA NOTA DE CREDITO A LA FACTURA QUE SE ESTA ITERANDO EN ESTE MOMENTO
                                    if fac.invoice_id.residual > nota.invoice_id.residual:
                                        fac.amount -= nota_de_credito.residual
                                    else:
                                        fac.amount -= fac.invoice_id.residual
                                    fac.invoice_id.assign_outstanding_credit(nota_credito_line.id)
                                if nota_de_credito.residual == 0:
                                    break

                for p in self.payment_ids.sorted(key=lambda r: r.amount, reverse=True):
                    diario = p.journal_id
                    if p.cheque_tercero:
                        if p.currency_id != p.moneda_pago:
                            moneda = p.moneda_pago.id
                        else:
                            moneda = p.currency_id.id
                        cheque_tercero = self.env['account.check.third'].search(
                            [('number', '=', p.numero_cheque_recibo),
                             ('bank_id', '=', p.banco_cheque_recibo.id)])
                        if not cheque_tercero:
                            cheque_tercero = self.env['account.check.third']

                            datos = {
                                'number': p.numero_cheque_recibo,
                                'amount': p.monto_cheque_recibo,
                                # 'issue_date': datetime.strftime(date.today(),"%d/%m/%Y"),
                                'bank_id': p.banco_cheque_recibo.id,
                                'cuit': p.nro_cuenta_recibo,
                                'payment_date': p.fecha_cheque_diferido,
                                'issue_date': p.fecha_cheque_recibo,
                                'tipo_cheque': p.tipo_de_cheque_recibo,
                                'voucher_id': p.id,
                                'journal_id': p.journal_id.id,
                                'recibo': p.recibo_id.name,
                                'source_partner_id': p.partner_id.id,
                                'owner_name': p.titular_recibo,
                                'currency_id': moneda,
                            }
                            cheque_tercero.create(datos)
                        else:
                            # raise ValidationError('No se puede duplicar numero de Cheque. Cheque nro %s ya existe en el sistema' % p.numero_cheque)
                            datos = {
                                'owner_name': p.titular_recibo,
                                'journal_id': p.journal_id.id,
                                'bank_id': p.banco_cheque_recibo.id,
                                'cuit': p.nro_cuenta_recibo,
                                'payment_date': p.fecha_cheque_diferido,
                                'issue_date': p.fecha_cheque_recibo,
                                'amount': p.monto_cheque_recibo + cheque_tercero.amount,
                                'tipo_cheque': p.tipo_de_cheque_recibo,
                                'number': p.numero_cheque_recibo,
                                'currency_id': moneda,
                            }
                            cheque_tercero.write(datos)

                    pago = p.amount

                    facturas = self.pagos_facturas_ids.filtered(
                        lambda r: r.invoice_id.residual > 0 and r.invoice_id.type not in (
                            'out_refund', 'in_refund'))

                    for i in facturas.sorted(key=lambda r: r.monto, reverse=True):
                        if pago > 0:
                            if not i.invoice_id.type in ('out_refund', 'in_refund'):
                                if i.amount == 0:
                                    i.verificar_amount()
                                if pago <= i.amount:
                                    i.amount -= pago
                                    i.invoice_id.monto_a_pagar = pago
                                    p.invoice_ids = [(4, i.invoice_id.id)]
                                    pago = 0
                                else:
                                    pago -= i.amount
                                    i.invoice_id.monto_a_pagar = i.amount
                                    p.invoice_ids = [(4, i.invoice_id.id)]
                                    i.amount = 0
                        else:
                            break
                    p.post_nuevo()
                    p.recibo_id = self.id
                if pago > 0:
                    if self.saldo != 0:
                        if self.saldo < 0:
                            self.asiento_utilidad(pago, diario, self.currency_id)
                        else:
                            ValidationError('Error al confirmar el recibo')
                if self.diferencia_cambio != 0:
                    self._crear_diferencia_cambio()
                # self.post_caja_recibo()
                self.state = 'confirmado'
                self.dias_en_borrador = 0
                # Los residuales se actualiza para la vista quede bien
                for i in self.pagos_facturas_ids:
                    if i.invoice_id.type in ('out_invoice', 'in_invoice'):
                        i.residual = i.invoice_id.residual
                    else:
                        i.residual = i.invoice_id.residual_signed
            else:
                raise ValidationError('No tiene asociado ninguna "Factura o Cobro" al Recibo')

    @api.multi
    def action_recibo_send(self):
        '''
        This function opens a window to compose an email, with the recibo template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('account_cobros_tech', 'email_template_recibo_cobro')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        lang = self.env.context.get('lang')
        template = template_id and self.env['mail.template'].browse(template_id)
        if template and template.lang:
            lang = template._render_template(template.lang, 'account.recibo', self.ids[0])
        ctx = {
            'default_model': 'account.recibo',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'model_description': 'Recibo',
           'custom_layout': "mail_notification_recibo",
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }