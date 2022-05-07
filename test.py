# -*- coding: utf-8 -*-

import unittest

import json
from ticketbai import TicketBai
from templates import *

PATH = '/home/juan/workspace/python/ticketbai'


class Testing(unittest.TestCase):

    @unittest.skip
    def test_vat(self):
        t = TicketBai(PATH)
        resul = t.get('vat/get/')
        self.assertEqual(t.response.status_code, 200)

    @unittest.skip
    def test_country(self):
        t = TicketBai(PATH)
        resul = t.get('country/get/')
        self.assertEqual(t.response.status_code, 200)

    @unittest.skip
    def test_customer(self):
        t = TicketBai(PATH)
        clavesIVA = ['"01"']
        data = {
            'nif': '51055347Q',
            'nombreoRazonSocial': 'Yanokito',
            'apellido1': 'Ma',
            'apellido2': 'Kaka',
            'municipio': 'Cóin',
            'codigoPostal': '29100',
            'direccion': 'Rue Percebe13',
            'email': 'si.@mail.com',
            'tipoLicencia': 'Basic',
            'clavesIVA': ','.join(clavesIVA),
            'tipoCertificado': 'Test'
        }

        resul = tcustomer.substitute(data)
        json_data = json.dumps(json.loads(resul))

        resul = t.put('customer/add', json_param=json_data)
        self.assertEqual(t.response.status_code, 200)

        resul = t.post('customer/cancel', url_list_param=['51055347Q'])
        self.assertEqual(t.response.status_code, 200)

        resul = t.get('customer/list')
        self.assertEqual(t.response.status_code, 200)

        resul = t.get('customer/info', ['51055347Q'])
        self.assertEqual(t.response.status_code, 200)

        # TODO:: esta mal, error 404
        # data = {
        #     'Nif': '51055347Q',
        #     'LicenseType': 'Basic'
        # }
        # json_data = json.dumps(data)
        # resul = t.post('customer/activate', json_param=json_data)
        # self.assertEqual(t.response.status_code, 200)

    def test_invoice(self):
        t = TicketBai(PATH)
        data = {
            'razonSocialONombre': 'Yanokito',
            'apellido1': 'Ma',
            'apellido2': 'Kaka',
            'nif': '51055347Q',
            'codigoPostal': '29100'
        }
        emisor = json.dumps(json.loads(temisor_factura.substitute(data)))

        extranjero = {}

        data = {
            'razonSocialONombreApellidos': 'Sin nombre ni apellidos',
            'nif': '87662841C',
            'codigoPostal': '29100',
            'direccion': 'Sin direción',
            'municipio': 'Coín',
            'destinatarioExtranjero': json.dumps(extranjero)

        }
        destinatario = json.dumps(json.loads(tdestinatario_factura.substitute(data)))

        data = {
            'tipoLineaContraparteNoNacional': 'Ninguna',
            'tipoSujecion': 'Ninguna',
            'causaExencionSujecionYNoSujecion': 'Ninguna',
            'concepto': 'El concepto',
            'precioUnitario': 10,
            'cantidad': 6,
            'descuentoSobreBaseImponible': 0,
            'porcentajeIva': 21,
            'recargoEquivalencia': 'false',
            'porcentajeRetencion': 0,
            'claveIVA': '01'
        }
        linea = json.dumps(json.loads(tlinea_factura.substitute(data)))

        data = {
            'produccion': 'false',
            'descripcion': 'Factura',
            'fechaOperacion': '2022-05-07T00:00:00.000Z',
            'fechaExpedicion': '2022-05-07T00:00:00.000Z',
            'serie': '2022',
            'numeroFactura': 1,
            'simplificada': 'true',
            'emisor': emisor,
            'destinatario': destinatario,
            'lineasFactura': linea
        }
        factura = json.dumps(json.loads(tfactura.substitute(data)))
        resul = t.put('invoice/send', factura)
        self.assertEqual(t.response.status_code, 200)

        params = ['87662841C', '2022', '1']
        resul = t.get('invoice/get', url_list_param=params)
        self.assertEqual(t.response.status_code, 200)

        params = ['87662841C', '2022', '1', 'false']
        resul = t.post('invoice/cancel', url_list_param=params)
        self.assertEqual(t.response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

