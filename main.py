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
                       tfactura, tfacturasRectificadasSustituidas, tfactura_correccion, tcustomer, tcustomer_activate)


__version__ = '0.0.1'


def conversion_caracter_basico(data):
    for origen, destino in [
        (chr(0xa0), chr(0xe1)),  # á
        (chr(0x82), chr(0xe9)),  # é
        (chr(0xa1), chr(0xed)),  # í
        (chr(0xa2), chr(0xf3)),  # ó
        (chr(0xa3), chr(0xfa)),  # ú
        (chr(0xa4), chr(0xf1)),  # ñ
        (chr(0xa5), chr(0xd1)),  # Ñ
        (chr(0xa7), chr(0xba)),  # º
        (chr(0xa6), chr(0xaa)),  # ª
        (chr(0x87), chr(0xe7)),  # ç
        (chr(0x80), chr(0xc7)),  # Ç
    ]:
        data = data.replace(origen, destino)
    return data


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
            status, resul = getattr(self, self.opcion)()
            data = json.dumps(resul, ensure_ascii=False, indent=4, sort_keys=True)
        except Exception as e:
            status = 'ko'
            data = f'[{datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")}] {e.__class__.__name__}: {e.args}'

        with open(log, modo, encoding='cp1252', errors='replace') as f:
            f.write(f'{self.opcion}\n{status}\n{data}\n')

    def certificate_add(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)

        param_data = {'Password': data[0]}

        with open(data[1], 'rb') as f:
            file = f.read()
        files = {'Certificate': file}

        param_url = [data[2]] if len(data) == 3 else None  # si hay nif

        return 'ok', self.send('post', 'certificate/add', param_data=param_data, files=files, param_url=param_url)

    def certificate_info(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)

        resul = self.send('get', 'certificate/info', param_url=data)
        status = 'ok' if resul.get('success') and not resul.get('errorMessage') else 'ko'
        return status, resul

    def vat_get(self):
        return 'ok', self.send('get', 'vat/get')

    def country_get(self):
        return 'ok', self.send('get', 'country/get')

    def customer_add(self):
        with open(self.fichero, 'r', encoding='cp1252') as f:
            data_str = conversion_caracter_basico(f.read())
            data = json.loads(data_str)

        for n, valores in enumerate(data):
            if n == 0:
                claves_iva = valores

            elif n == 1:
                valores.append(json.dumps(claves_iva))
                keys = ['nif', 'nombreoRazonSocial', 'apellido1', 'apellido2', 'municipio', 'codigoPostal',
                        'direccion', 'email', 'tipoLicencia', 'tipoCertificado', 'clavesIVA']
                data = dict(zip(keys, valores))
                customer = json.loads(tcustomer.substituye(data))
                resul = self.send('put', 'customer/add', param_json=customer)
                status = 'ok' if resul.get('success') and not resul.get('errorMessage') else 'ko'
                return status, resul

    def customer_list(self):
        return 'ok', self.send('get', 'customer/list')

    def customer_cancel(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        return 'ok', self.send('post', 'customer/cancel', param_url=data)

    def customer_info(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)

        resul = self.send('get', 'customer/info', param_url=data)
        status = 'ok' if resul.get('success') and not resul.get('errorMessage') else 'ko'
        return status, resul

    def customer_activate(self):
        with open(self.fichero, 'r') as f:
            valores = json.load(f)

        keys = ['Nif', 'LicenseType']
        data = dict(zip(keys, valores))
        activate = json.loads(tcustomer_activate.substituye(data))
        resul = self.send('post', 'customer/activate', param_data=activate)
        status = 'ok' if resul.get('success') and not resul.get('errorMessage') else 'ko'
        return status, resul

    def invoice_send(self):
        with open(self.fichero, 'r', encoding='cp1252') as f:
            data_str = conversion_caracter_basico(f.read())
            data = json.loads(data_str)

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
                    extranjero = json.loads(tdestinatario_factura_extranjero.substituye(data))

            elif n == 2:
                destinatario = dict()
                if valores:
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
                factura = json.loads(tfactura.substituye(data))
                resul = self.send('put', 'invoice/send', param_json=factura)
                status = 'ok' if resul.get('success') and not resul.get('errrores') else 'ko'
                return status, resul

    def invoice_get(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        resul = self.send('get', 'invoice/get', param_url=data)
        status = 'ok' if resul.get('success') and not resul.get('message') else 'ko'
        return status, resul

    def invoice_cancel(self):
        with open(self.fichero, 'r') as f:
            data = json.load(f)
        resul = self.send('post', 'invoice/cancel', param_url=data)
        status = 'ok' if resul.get('success') and not resul.get('errrores') else 'ko'
        return status, resul

    def invoice_correct(self):
        with open(self.fichero, 'r', encoding='cp1252') as f:
            data_str = conversion_caracter_basico(f.read())
            data = json.loads(data_str)

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
                destinatario = dict()
                if valores:
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
                if valores:
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
                factura = json.loads(tfactura_correccion.substituye(data))
                resul = self.send('post', 'invoice/correct', param_json=factura)
                status = 'ok' if resul.get('success') and not resul.get('errrores') else 'ko'
                return status, resul


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-u', '--usuario', dest='usuario', type=str, help='Usuario', required=False)
    parser.add_argument('-c', '--clave', dest='clave', type=str, help='Clave', required=False)
    parser.add_argument('-l', '--log', dest='log', type=str, help='Fichero log', required=False)
    parser.add_argument('-f', '--fichero', dest='fichero', type=str, help='Fichero de datos (log si no se informa)', required=True)
    parser.add_argument('-o', '--opcion', dest='opcion', type=str, help='Opción a ejecutar', required=True)
    Main(parser.parse_args())
