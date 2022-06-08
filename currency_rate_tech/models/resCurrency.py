# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from num2words import num2words
import json
from datetime import datetime, timedelta
import requests
import urllib3
from decimal import Decimal
from bs4 import BeautifulSoup
import re
import logging

_logger = logging.getLogger(__name__)


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def format_decimal(number):
    return str(number).replace(".", "").replace(",", ".")


def setgov():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        soup = BeautifulSoup(
            requests.get(
                "http://www.set.gov.py/portal/PARAGUAY-SET", timeout=10).text,
            "html.parser",
        )
        compra_texto = soup.select("div#main>div.UITipoGrafiaCotizacion:nth-of-type(1)>div")[1].text.replace(
            "G. ", "").replace(".", "").replace(',', '.')
        compra = (re.findall("\d+\.\d+", compra_texto)[0])

        venta_texto = soup.select("div#main>div.UITipoGrafiaCotizacion:nth-of-type(1)>div")[2].text.replace(
            "G. ", "").replace(".", "").replace(',', '.')
        venta = (re.findall("\d+\.\d+", venta_texto)[0])
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


def bcp():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        soup = BeautifulSoup(
            requests.get(
                "https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante",
                timeout=10,
                headers={"user-agent": "Mozilla/5.0"},
                verify=False,
            ).text,
            "html.parser",
        )
        fecha = soup.find('input', {'id': 'dp_cotizacion'}).get('value')
        if fecha:
            fecha_obj = datetime.strptime(fecha, '%d/%m/%Y').date()
        else:
            fecha_obj = None
        compra_array = soup.find(
            class_="table table-striped table-bordered table-condensed"
        ).select("tfoot > tr > th:nth-of-type(2)")
        venta_array = soup.find(
            class_="table table-striped table-bordered table-condensed"
        ).select("tfoot > tr > th:nth-of-type(3)")
        if len(compra_array) > 0:
            posicion = len(compra_array) - 1
            compra = compra_array[posicion].get_text().replace(
                ".", "").replace(",", ".")
            venta = venta_array[posicion].get_text().replace(
                ".", "").replace(",", ".")
        else:
            compra, venta = 0, 0
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta), fecha_obj


def create_json(self):
    setcompra, setventa, fecha = bcp()
    respjson = {
        "dolarpy": {
            "bcp": {"compra": setcompra, "venta": setventa},
        },
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return json.dumps(
        respjson,
        indent=4,
        sort_keys=True,
        separators=(",", ": "),
        default=self.decimal_default(),
    )


def get_output():
    with open("dolar.json", "r") as f:
        response = f.read()
    return response


def write_output():
    response = create_json()
    with open("dolar.json", "w") as f:
        f.write(response)


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    @api.model
    def registrar_cotizacion_compra_venta_set(self):
        compra, venta, fecha_cotizacion = bcp()
        fecha_actual = fields.Date.today()
        fecha_cotizacion_technoma = fecha_actual + timedelta(days=1)
        currency_compra_id = self.env['res.currency'].search([('name', 'ilike', 'USD COMPRA')], limit=1).id
        currency_venta_id = self.env['res.currency'].search([('name', 'ilike', 'USD VENTA')], limit=1).id
        tasa_compra = self.search([('name', '=', fecha_cotizacion_technoma), ('currency_id', '=', currency_compra_id)])
        tasa_venta = self.search([('name', '=', fecha_cotizacion_technoma), ('currency_id', '=', currency_venta_id)])

        # if fecha_actual.weekday() in (
        # 5, 6):  # Si la fecha actual es sabado o domingo (No existe cotizacion en la set, se toma la
            # del viernes)
            # Se cargan los valores originales cotizacion compra y venta de la set desde lo ultimo registrado en odoo
            # venta = self.search([('currency_id', '=', currency_compra_id)], order='id desc', limit=1)
            # compra = self.search([('currency_id', '=', currency_compra_id)], order='id desc', limit=1)
            # fecha_cotizacion = fecha_actual

        if not tasa_compra and not tasa_venta:
            if compra > 0 and venta > 0 and fecha_actual == fecha_cotizacion:
                rate_compra = 1 / compra
                rate_venta = 1 / venta
                tasa_compra_car = self.sudo().create({'name': fecha_cotizacion_technoma,
                                               'currency_id': currency_compra_id,
                                               'rate': rate_venta,
                                               'set_venta': venta
                                               })
                tasa_venta_car = self.sudo().create({'name': fecha_cotizacion_technoma,
                                              'currency_id': currency_venta_id,
                                              'rate': rate_compra,
                                              'set_venta': compra
                                              })

                if not (tasa_compra_car and tasa_venta_car):
                    _logger.error('No se pudo crear la cotizacion del dia % s' % fecha_cotizacion_technoma)
                    return False
                else:
                    currency_compra_id = self.env['res.currency'].search([('name', 'ilike', 'USD COMPRA')], limit=1)
                    currency_venta_id = self.env['res.currency'].search([('name', 'ilike', 'USD VENTA')], limit=1)
                    return fecha_cotizacion_technoma, currency_compra_id.name, venta, currency_venta_id.name, compra
            else:
                _logger.error(
                    'No se pudo crear la cotizacion del dia % s. No es posible acceder a la cotizacion de la fecha.' % fecha_cotizacion_technoma)
                return False
        else:
            _logger.info('Ya existe una cotizacion registrada en la fecha %s' % fecha_cotizacion_technoma)
            return False
