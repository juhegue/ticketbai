# -*- coding: utf-8 -*-

import io
import os
import sys
import json
import logging
import requests
from datetime import datetime, timezone
from templates import *

"""
Entorno OpenApi: https://apipartner.ticketbai.pro/swagger/index.html
"""

URL_IDENTITY = 'https://login.consulpyme.com/connect/token'
URL_TICKETBAI = 'https://apipartner.ticketbai.pro/api'


class TicketBai:
    response = None

    def __init__(self, cwd=None):
        path = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]
        self.path = cwd or os.path.split(path)[0]
        self.token, self.token_type = self._get_token(self._get_config())

    def _get_config(self):
        fic = os.path.join(self.path, 'config.json')
        with open(fic, 'rb') as f:
            data = json.load(f)
        return data

    def _get_token(self, config):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': config.get('client_id'),
            'client_secret': config.get('client_secret'),
            'scope': 'api_ticketbaipro'
        }
        response = requests.post(URL_IDENTITY, headers=headers, data=data)
        if 200 <= response.status_code <= 299:
            resul = json.loads(response.text)
            return resul.get('access_token'), resul.get('token_type')
        else:
            error = json.loads(response.text).get('error_description')
            print(f'ERROR (get_token)= {response.status_code} {response.reason}:{error}')
            quit(-1)

    def _response(self, tipo, url, data=None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'{self.token_type} {self.token}'
        }

        if tipo == 'get':
            response = requests.get(url, headers=headers)
        elif tipo == 'post':
            response = requests.post(url, headers=headers, data=data or {})
        elif tipo == 'put':
            response = requests.put(url, headers=headers, data=data or {})
        else:
            raise Exception(f'Tipo no definido: {tipo}')

        self.response = response
        if 200 <= response.status_code <= 299:
            return json.loads(response.text)
        else:
            print(f'ERROR ({url})= {response.status_code}:{response.reason}')

    def get(self, funcion, url_list_param=None):
        url = f'{URL_TICKETBAI}/{funcion}'
        if url_list_param:
            url += '/' + '/'.join(url_list_param)
        return self._response('get', url)

    def post(self, funcion, url_list_param=None, json_param=None):
        url = f'{URL_TICKETBAI}/{funcion}'
        if url_list_param:
            url += '/' + '/'.join(url_list_param)
        return self._response('post', url, json_param)

    def put(self, funcion, json_param):
        url = f'{URL_TICKETBAI}/{funcion}'
        return self._response('put', url, json_param)


if __name__ == '__main__':
    t = TicketBai()
    vat = t.get('vat/get/')
    print(vat)
