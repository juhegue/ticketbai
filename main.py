# -*- coding: utf-8 -*-

import argparse
import json
from ticketbai import TicketBai
from templates import *

"""
Envio factura a TicketBai
"""

__version__ = '0.0.1'

def main():
    ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-f', '--fichero', dest='fichero', type=str, help='Fichero de datos', required=True)
    parser.add_argument('-o', '--opcion', dest='opcion', type=str, help='Opción a ejecutar', required=True)
    args = parser.parse_args()
    main()
