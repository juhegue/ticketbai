# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import hashlib
import pathlib
import pickle
import requests

"""
Entorno OpenApi: https://apipartner.ticketbai.pro/swagger/index.html
"""

URL_IDENTITY = 'https://login.consulpyme.com/connect/token'
URL_TICKETBAI = 'https://apipartner.ticketbai.pro/api'

logger = logging.getLogger(__name__)


class TicketBai:
    response = None

    def __init__(self, cwd=None):
        path = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]
        self.path = cwd or os.path.split(path)[0]
        self.client_id, self.client_secret = self._get_config()
        self.token, self.token_type = self.get_token_type()

    def _get_config(self):
        fic = os.path.join(self.path, 'config.json')
        with open(fic, 'rb') as f:
            data = json.load(f)
        return data.get('client_id'), data.get('client_secret')

    def token(self):
        try:
            tokens = self._get_tokens_local()
            md5 = self._get_md5()
            return tokens[md5]
        except:
            return self._get_token_identity()

    @staticmethod
    def _get_home_config():
        home = pathlib.Path.home()
        nombre = os.path.basename(__file__).split('.')[0]
        fichero = os.path.join(home, f'.{nombre}')
        return fichero

    def get_token_type(self):
        try:
            tokens = self._get_tokens_local()
            md5 = self._get_md5()
            return tokens[md5]
        except:
            access_token, token_type = self._get_token_identity()
            self.set_token_type(access_token, token_type)
            return access_token, token_type

    def set_token_type(self, token, type):
        fichero = self._get_home_config()
        try:
            tokens = self._get_tokens_local()
            md5 = self._get_md5()
            tokens[md5] = token, type
            with open(fichero, 'wb') as f:
                pickle.dump(tokens, f)
        except:
            pass

    def _get_tokens_local(self):
        fichero = self._get_home_config()
        try:
            with open(fichero, 'rb') as f:
                data = pickle.load(f)
            return data
        except:
            return dict()

    def _get_md5(self):
        return hashlib.md5(f'{self.client_id}{self.client_secret}'.encode('utf-8')).hexdigest()

    def _get_token_identity(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
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
            return json.loads(response.text or '{}')
        elif response.status_code == 401:
            access_token, token_type = self._get_token_identity()
            self.set_token_type(access_token, token_type)
            return self._response(tipo, url, data)
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

