# -*- coding: utf-8 -*-

import unittest

import json
from ticketbai import TicketBai
from templates import *

PATH = '/home/juan/workspace/python/ticketbai'


class Testing(unittest.TestCase):

    def test_vat(self):
        t = TicketBai(PATH)
        resul = t.get('vat/get/')
        self.assertEqual(t.response.status_code, 200)

    def test_country(self):
        t = TicketBai(PATH)
        resul = t.get('country/get/')
        self.assertEqual(t.response.status_code, 200)

    def test_customer(self):
        t = TicketBai(PATH)

        clavesIVA = ['"01"']
        data = {
            "nif": "51055347Q",
            "nombreoRazonSocial": "Yanokito",
            "apellido1": "Ma",
            "apellido2": "Kaka",
            "municipio": "Cóin",
            "codigoPostal": "29100",
            "direccion": "Rue Percebe13",
            "email": "si.@mail.com",
            "tipoLicencia": "Basic",
            "clavesIVA": ",".join(clavesIVA),
            "tipoCertificado": "Test"
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

        data = {
            "Nif": '51055347Q',
            "LicenseType": "Basic"
        }
        json_data = json.dumps(data)
        resul = t.post('customer/activate', json_param=json_data)
        self.assertEqual(t.response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

