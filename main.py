# -*- coding: utf-8 -*-

"""
Envio factura a TicketBai
(juhegue vie 6 may 2022)
"""

import argparse
import datetime
import json
from ticketbai import TicketBai
from templates import (temisor_factura, tdestinatario_factura_extranjero, tdestinatario_factura, tlinea_factura,
                       tfactura, tfacturasRectificadasSustituidas, tfactura_correccion, tcustomer)


__version__ = '0.0.1'


class Main(TicketBai):
    def __init__(self, args):
        self.fichero = args.fichero
        self.opcion = args.opcion
        log, modo = (args.log, 'a') if hasattr(args, 'log') and args.log else (args.fichero, 'w')

        kwargs = dict()
        if hasattr(args, 'usuario') and hasattr(args, 'clave') and args.usuario and args.clave:
            kwargs = {'usuario': args.usuario, 'clave': args.clave}
        if hasattr(args, 'cwd'):
            kwargs.update({'cwd': args.cwd})
        super().__init__(**kwargs)

        try:
            resul = getattr(self, self.opcion)()
            data = json.dumps(resul, indent=4, sort_keys=True)
        except Exception as e:
            data = f'[{datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")}] {e.__class__.__name__}: {e.args}'

        with open(log, modo) as f:
            f.write(f'{self.opcion}\n{data}\n')

    def vat_get(self):
        return self.get('vat/get/')

    def country_get(self):
        return self.get('country/get/')

    def customer_list(self):
        return self.get('customer/list/')

    def customer_add(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)

        for n, valores in enumerate(data):
            if n == 0:
                claves_iva = valores

            elif n == 1:
                valores.append(json.dumps(claves_iva))
                keys = ['nif', 'nombreoRazonSocial', 'apellido1', 'apellido2', 'municipio', 'codigoPostal',
                        'direccion', 'email', 'tipoLicencia', 'tipoCertificado', 'clavesIVA']
                data = dict(zip(keys, valores))
                customer = json.dumps(json.loads(tcustomer.substituye(data)))
                resul = self.put('customer/add', customer)
                return resul

    def customer_cancel(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        return self.post('customer/cancel', url_list_param=data)

    def customer_info(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        return self.get('customer/info', data)

    def invoice_send(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)

        for n, valores in enumerate(data):
            if n == 0:
                keys = ['razonSocialONombre', 'apellido1', 'apellido2', 'nif', 'codigoPostal']
                data = dict(zip(keys, valores))
                emisor = json.loads(temisor_factura.substituye(data))

            elif n == 1:
                extranjero = dict()
                if valores:
                    keys = ['pais', 'identificacion', 'claveIdentificacionPaísResidencia']
                    data = dict(zip(keys, valores))
                    extranjero = json.loads(temisor_factura.substituye(data))

            elif n == 2:
                valores.append(json.dumps(extranjero))
                keys = ['razonSocialONombreApellidos', 'nif', 'codigoPostal', 'direccion', 'municipio',
                        'destinatarioExtranjero']
                data = dict(zip(keys, valores))
                destinatario = json.loads(tdestinatario_factura.substituye(data))

            elif n == 3:
                lineas = list()
                keys = ['tipoLineaContraparteNoNacional', 'tipoSujecion', 'causaExencionSujecionYNoSujecion',
                        'concepto', 'precioUnitario', 'cantidad', 'descuentoSobreBaseImponible', 'porcentajeIva',
                        'recargoEquivalencia', 'porcentajeRetencion', 'claveIVA']
                for l in valores:
                    data = dict(zip(keys, l))
                    linea = json.loads(tlinea_factura.substituye(data))
                    lineas.append(linea)

            elif n == 4:
                valores.append(json.dumps(emisor))
                valores.append(json.dumps(destinatario))
                valores.append(json.dumps(lineas))
                keys = ['produccion', 'descripcion', 'fechaOperacion', 'fechaExpedicion', 'serie', 'numeroFactura',
                        'simplificada', 'emisor', 'destinatario', 'lineasFactura']
                data = dict(zip(keys, valores))
                factura = json.dumps(json.loads(tfactura.substituye(data)))
                resul = self.put('invoice/send', factura)
                return resul

    def invoice_get(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        return self.get('invoice/get', url_list_param=data)

    def invoice_cancel(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        return self.post('invoice/cancel', url_list_param=data)

    def invoice_correccion(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)

        for n, valores in enumerate(data):
            if n == 0:
                keys = ['razonSocialONombre', 'apellido1', 'apellido2', 'nif', 'codigoPostal']
                data = dict(zip(keys, valores))
                emisor = json.loads(temisor_factura.substituye(data))

            elif n == 1:
                extranjero = dict()
                if valores:
                    keys = ['pais', 'identificacion', 'claveIdentificacionPaísResidencia']
                    data = dict(zip(keys, valores))
                    extranjero = json.loads(temisor_factura.substituye(data))

            elif n == 2:
                valores.append(json.dumps(extranjero))
                keys = ['razonSocialONombreApellidos', 'nif', 'codigoPostal', 'direccion', 'municipio',
                        'destinatarioExtranjero']
                data = dict(zip(keys, valores))
                destinatario = json.loads(tdestinatario_factura.substituye(data))

            elif n == 3:
                lineas = list()
                keys = ['tipoLineaContraparteNoNacional', 'tipoSujecion', 'causaExencionSujecionYNoSujecion',
                        'concepto', 'precioUnitario', 'cantidad', 'descuentoSobreBaseImponible', 'porcentajeIva',
                        'recargoEquivalencia', 'porcentajeRetencion', 'claveIVA']
                for l in valores:
                    data = dict(zip(keys, l))
                    linea = json.loads(tlinea_factura.substituye(data))
                    lineas.append(linea)

            elif n == 4:
                rectificadas = list()
                keys = ['serie', 'numero', 'fechaExpedicion']
                for l in valores:
                    data = dict(zip(keys, l))
                    linea = json.loads(tfacturasRectificadasSustituidas.substituye(data))
                    rectificadas.append(linea)

            elif n == 5:
                valores.append(json.dumps(emisor))
                valores.append(json.dumps(destinatario))
                valores.append(json.dumps(lineas))
                valores.append(json.dumps(rectificadas))
                keys = ['produccion', 'descripcion', 'fechaOperacion', 'fechaExpedicion', 'serie', 'numeroFactura',
                        'simplificada', 'facturaEmitidaSustitucionSimplificada', 'codigoFacturaRectificativa',
                        'tipoFacturaRectificativa', 'baseRectificativa', 'cuotaRectificada', 'cuotaRecargoRectificada',
                        'emisor', 'destinatario', 'lineasFactura', 'facturasRectificadasSustituidas']
                data = dict(zip(keys, valores))
                factura = json.dumps(json.loads(tfactura_correccion.substituye(data)))
                resul = self.put('invoice/send', factura)
                return resul


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-u', '--usuario', dest='usuario', type=str, help='Usuario', required=False)
    parser.add_argument('-c', '--clave', dest='clave', type=str, help='Clave', required=False)
    parser.add_argument('-l', '--log', dest='log', type=str, help='Fichero log', required=False)
    parser.add_argument('-f', '--fichero', dest='fichero', type=str, help='Fichero de datos (log si no se informa)', required=True)
    parser.add_argument('-o', '--opcion', dest='opcion', type=str, help='Opción a ejecutar', required=True)
    Main(parser.parse_args())
