# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp
from num2words import num2words


# class Factura_invoice(models.Model):
    # _inherit = 'account.check.third'
    #
    #
    # cuit = fields.Char(string="Nro. de Cuenta",required=False)
    # tipo_cheque = fields.Selection([('diferido','Diferido'),('vista','A la vista')],string="Tipo de cheque",compute='_set_tipo_cheque')
    # bank_id = fields.Many2one(
    #     'res.bank', 'Banco',
    #     readonly=False,
    #     track_visibility="onchange"
    # )
    # number = fields.Integer(
    #     'Numero',
    #     required=True,
    #     readonly=False,
    #     track_visibility="onchange",
    #     copy=False
    # )
    # amount = fields.Float(
    #     'Monto',
    #     required=True,
    #     readonly=True,
    #     track_visibility="onchange",
    #     digits=dp.get_precision('Account'),
    #     states={'handed': [('readonly', False)]}
    # )
    # owner_name = fields.Char(
    #     'Propietario',
    #     readonly=False,
    #     track_visibility="onchange",
    #     states={'handed': [('readonly', False)]}
    # )
    # payment_date = fields.Date(
    #     'Fecha de pago',
    #     readonly=False,
    #     track_visibility="onchange",
    #     help="Only if this check is post dated",
    #     states={'handed': [('readonly', False)]}
    # )
    # issue_date = fields.Date(
    #     'Fecha de Emision',
    #     readonly=False,
    #     states={'handed': [('readonly', False)]},
    #     track_visibility="onchange"
    # )
    #
    # @api.onchange('voucher_id')
    # def _set_cuit(self):
    #     cuenta = self.env['res.partner.bank'].search([('partner_id','=',self.voucher_id.partner_id.id)],limit=1)
    #     if cuenta:
    #         self.cuit = cuenta.acc_number
    #         self.owner_name= cuenta.titular
    #         self.bank_id = cuenta.bank_id
    #
    # @api.onchange('issue_date','payment_date')
    # def _set_tipo_cheque(self):
    #     if self.issue_date and self.payment_date:
    #         if self.issue_date != self.payment_date:
    #             self.tipo_cheque = 'diferido'
    #         else:
    #             self.tipo_cheque ='vista'
    #     elif self.issue_date:
    #         self.tipo_cheque='vista'

class Cheques(models.Model):
    _inherit = 'account.check'

    def agregar_punto_de_miles(self, numero):
        numero_con_punto = '.'.join([str(int(numero))[::-1][i:i + 3] for i in range(0, len(str(int(numero))), 3)])[::-1]
        return numero_con_punto

    def calcular_letras(self, numero):
        letras = self.monto_en_letras = num2words(numero, lang='es').upper()
        letras = letras + '--'
        return letras

    def dia(self, fecha):
        if (fecha):
            cadena = str(fecha)

            return cadena[8:10]

    def mes(self, fecha):
        if (fecha):
            cadena = str(fecha)

            return cadena[5:7]

    def ano(self, fecha):
        if (fecha):
            cadena = str(fecha)

            return cadena[2:4]

    def cantidaddecaracteres35(self, a):
        b = str(a)
        return b[0:35]

    def cantidaddecaracteres30(self, a):
        b = str(a)
        return b[0:30]

    def cantidaddecaracteres24(self, a):
        b = str(a)
        return b[0:24]

    def cantidaddecaracteres55(self, a):
        b = str(a)
        return b[0:70]