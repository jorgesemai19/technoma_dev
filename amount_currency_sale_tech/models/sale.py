# -*- coding: utf-8 -*-

import re

from odoo import api, models, fields, _


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        currency_rates = (from_currency + to_currency)._get_rates(company, date)
        res = currency_rates.get(to_currency.id) / currency_rates.get(from_currency.id)
        return res


class PurchaseCurrency(models.Model):
    _inherit = 'sale.order'

    company_currency = fields.Many2one('res.currency',
                                       default=lambda self: self.env.user.company_id.currency_id)
    currency_usd = fields.Many2one('res.currency',
                                   default=lambda self: self._get_default_moneda_usd())
    company_currency_amount_total = fields.Monetary(string='Total Gs', compute='find_amount',
                                                    currency_field='company_currency', store=True)
    company_currency_amount_untaxed = fields.Monetary(string='Total sin IVA Gs', compute='find_amount',
                                                      currency_field='company_currency', store=True)
    company_currency_amount_tax = fields.Monetary(string='IVA Gs', compute='find_amount',
                                                  currency_field='company_currency', store=True)
    amount_total_usd = fields.Monetary(string='Total $', compute='find_amount', currency_field='currency_usd',
                                       store=True)
    amount_untaxed_usd = fields.Monetary(string='Total sin IVA $', compute='find_amount', currency_field='currency_usd',
                                         store=True)
    amount_tax_usd = fields.Monetary(string='IVA $', compute='find_amount', currency_field='currency_usd', store=True)
    cotizacion = fields.Float(string='Cotizacion', compute='get_cotizacion', store=True)

    @api.onchange('date_order')
    def get_cotizacion(self):
        for rec in self:
            currency_id = self.env['res.currency'].search([('name', 'ilike', 'USD'), ('ambito', '=', 'venta')],
                                                          limit=1).id
            cotizacion = self.env['res.currency.rate'].search([('currency_id', '=', currency_id), ('name', '=',
                                                                                                    rec.date_order.date())],
                                                              limit=1)
            rec.cotizacion = cotizacion.set_venta

    def find_amount(self):
        for rec in self:
            currency_id = rec.pricelist_id.currency_id
            rate_date = rec.date_order.date() or fields.Date.today()
            if rec.pricelist_id.currency_id and rec.company_id and rec.pricelist_id.currency_id != rec.company_id.currency_id:
                rec.company_currency_amount_total = currency_id._convert(rec.amount_total, rec.company_id.currency_id,
                                                                         rec.company_id, rate_date)
                rec.company_currency_amount_untaxed = currency_id._convert(rec.amount_untaxed,
                                                                           rec.company_id.currency_id,
                                                                           rec.company_id, rate_date)
                rec.company_currency_amount_tax = currency_id._convert(rec.amount_tax, rec.company_id.currency_id,
                                                                       rec.company_id, rate_date)
                rec.amount_total_usd = rec.amount_total
                rec.amount_untaxed_usd = rec.amount_untaxed
                rec.amount_tax_usd = rec.amount_tax

            else:
                rec.company_currency_amount_total = rec.amount_total
                rec.company_currency_amount_untaxed = rec.amount_untaxed
                rec.company_currency_amount_tax = rec.amount_tax
                rec.amount_total_usd = currency_id._convert(rec.amount_total, rec.currency_usd, rec.company_id,
                                                            rate_date)
                rec.amount_untaxed_usd = currency_id._convert(rec.amount_untaxed, rec.currency_usd, rec.company_id,
                                                              rate_date)
                rec.amount_tax_usd = currency_id._convert(rec.amount_tax, rec.currency_usd, rec.company_id,
                                                          rate_date)

    @api.model
    def _get_default_moneda_usd(self):
        moneda = self.env['res.currency'].search([('name', 'ilike', 'USD'), ('ambito', '=', 'venta')], limit=1).id
        return moneda
