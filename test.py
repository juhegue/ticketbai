# -*- coding: utf-8 -*-

import unittest

import os
import sys
from main import Main

funcion = lambda: sys._getframe(1).f_code.co_name[5:]

PATH = '/home/juan/workspace/python/ticketbai'


class Args:
    cwd = PATH
    log = os.path.join('/tmp', 'ticketbai.log')

    def __init__(self, opcion, fichero):
        self.opcion = opcion
        self.fichero = fichero


class Testing(unittest.TestCase):

    @unittest.skip
    def test_vat_get(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    @unittest.skip
    def test_country_get(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    @unittest.skip
    def test_customer_add(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    @unittest.skip
    def test_customer_list(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    @unittest.skip
    def test_customer_cancel(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    @unittest.skip
    def test_customer_info(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    @unittest.skip  # TODO:: esta mal da un 400
    def test_customer_activate(self):
        args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
        m = Main(args)
        self.assertEqual(m.status_code, 200)

    # def test_invoice_send(self):
    #     args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
    #     m = Main(args)
    #     self.assertEqual(m.status_code, 200)
    #
    # def test_invoice_get(self):
    #     args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
    #     m = Main(args)
    #     self.assertEqual(m.status_code, 200)
    #
    # def test_invoice_cancel(self):
    #     args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
    #     m = Main(args)
    #     self.assertEqual(m.status_code, 200)
    #
    # def test_invoice_correct(self):
    #     args = Args(funcion(), os.path.join(PATH, 'json', f'{funcion()}.json'))
    #     m = Main(args)
    #     self.assertEqual(m.status_code, 200)


if __name__ == '__main__':
    unittest.main()
