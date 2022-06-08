# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from num2words import num2words


class remision(models.Model):
    _inherit = "stock.picking"


    @api.model
    def _default_direccion_salida(self):
        return self.env.user.company_id.street

    @api.model
    def _default_ciudad_salida(self):
        return self.env.user.company_id.city

    @api.model
    def _default_departamento_salida(self):
        return self.env.user.company_id.state_id.name

    @api.multi
    @api.model
    def _default_direccion_llegada(self):
        if self.partner_id:
            domicilio = ''
            street1 = self.partner_id.street
            street2 = self.partner_id.street2
            if street1:
                domicilio += street1
            if street2:
                domicilio += street2
            return domicilio

    @api.model
    def _default_ciudad_llegada(self):
        if self.partner_id:
            return self.partner_id.city

    @api.model
    def _default_departamento_llegada(self):
        if self.partner_id:
            return self.partner_id.state_id.name

    motivo_translado = fields.Selection([('venta', 'Venta'), ('leasing', 'Leasing'), ('prestamo', 'Prestamo')],
                                        track_visibility='onchange')
    fecha_inicio_traslado = fields.Date(track_visibility='onchange')
    fecha_fin_traslado = fields.Date(track_visibility='onchange')
    direccion_salida = fields.Char(default=_default_direccion_salida, track_visibility='onchange')
    ciudad_salida = fields.Char(default=_default_ciudad_salida, track_visibility='onchange')
    departamento_salida = fields.Char(default=_default_departamento_salida, track_visibility='onchange')
    direccion_llegada = fields.Char(default=_default_direccion_llegada, track_visibility='onchange')
    ciudad_llegada = fields.Char(default=_default_ciudad_llegada, track_visibility='onchange')
    departamento_llegada = fields.Char(default=_default_departamento_llegada, track_visibility='onchange')

    @api.onchange('scheduled_date')
    def cambio_fecha_inicio_fin_traslado(self):
        if not self.fecha_inicio_traslado and self.scheduled_date:
            self.fecha_inicio_traslado = self.scheduled_date.date()
        if not self.fecha_fin_traslado and self.scheduled_date:
            self.fecha_fin_traslado = self.scheduled_date.date()

    @api.onchange('partner_id')
    def cambio_partner(self):
        domicilio = ''
        street1 = self.partner_id.street
        street2 = self.partner_id.street2
        if street1:
            domicilio += street1
        if street2:
            domicilio += street2

        self.direccion_llegada = domicilio
        self.ciudad_llegada = self.partner_id.city
        self.departamento_llegada = self.partner_id.state_id.name

    @api.multi
    def borrar_nro_remision(self):
        for picking in self:
            moves_to_backorder = picking.move_lines
            if moves_to_backorder:
                picking.numero_remision = None
                picking.talonario_remision = None

    @api.multi
    def get_procesar_producto(self, lista_producto):
        longitud = len(lista_producto)
        print("Longitud: " + str(longitud))
        return longitud

    @api.multi
    def get_prueba(self, tipo):
        tipo = type(tipo)
        bandera = 0
        if (tipo is str):
            bandera = 1
        elif (tipo is True):
            bandera = 0
        elif (tipo is False):
            bandera = 0
        # print(tipo)
        print(bandera)
        return bandera

    @api.multi
    def get_descripcion(self, producto):
        descripcion = ''
        if (type(producto.display_type) is str):
            descripcion = producto.name
        return descripcion

    def _get_fecha(self):
        hora = fields.Datetime.now()
        return (hora)

    def get_remision_data(self):
        remision = self
        datos = list()
        print(remision)
        dato_final = 'None'
        for orden in remision:
            datos.append(orden.numero_remision)
            datos.append(orden.talonario_remision.name)
            datos.append(orden.talonario_remision.fecha_inicio)
            datos.append(orden.talonario_remision.fecha_final)
            dato_final = orden.talonario_remision.name
            print(orden.talonario_remision.name)
            print(datos)

        return datos

    def sacacoma(self, n):
        return int(n)

    @api.multi
    def agregar_punto_de_miles_2(self, numero):
        numero_con_punto = '.'.join([str(int(numero))[::-1][i:i + 3] for i in range(0, len(str(int(numero))), 3)])[::-1]
        return numero_con_punto

    def agregar_punto_de_miles(self, numero, moneda):
        entero = int(numero)
        if 'USD' in moneda:

            decimal = '{0:.2f}'.format(numero - entero)
            entero_string = '.'.join([str(int(entero))[::-1][i:i + 3] for i in range(0, len(str(int(entero))), 3)])[
                            ::-1]
            if decimal == '0.00':
                numero_con_punto = entero_string + ',00'
            else:
                decimal_string = str(decimal).split('.')
                numero_con_punto = entero_string + ',' + decimal_string[1]
        elif 'PYG' in moneda:
            numero_con_punto = '.'.join([str(int(numero))[::-1][i:i + 3] for i in range(0, len(str(int(numero))), 3)])[
                               ::-1]
            return numero_con_punto
        else:
            numero_con_punto = '.'.join([str(int(numero))[::-1][i:i + 3] for i in range(0, len(str(int(entero))), 3)])[
                               ::-1]
        num_return = numero_con_punto
        return num_return

    def calcula_moneda(self, moneda):
        if 'USD' in moneda:
            return '$'
        elif 'PYG' in moneda:
            return 'Gs.'

    @api.multi
    def get_nro_factura(self):
        factura = ''
        if self.factura_ids:
            factura = self.factura_ids[0].nro_factura
        return factura

    @api.multi
    def get_nro_timbrado(self):
        nro_timbrado = ''
        if self.factura_ids:
            nro_timbrado = self.factura_ids[0].timbrado
        return nro_timbrado

    @api.multi
    def get_fecha_expedicion_factura(self):
        fecha_expedicion = ''
        if self.factura_ids:
            fecha_expedicion = self.factura_ids[0].date_invoice.strftime('%d/%m/%Y')
        return fecha_expedicion