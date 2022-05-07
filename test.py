# -*- coding: utf-8 -*-

import unittest

from ticketbai import TicketBai

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
        resul = t.get('customer/list')
        self.assertEqual(t.response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

