# -*- coding: utf-8 -*-

"""
Comunicación con TicketBai
(juhegue vie 6 may 2022)
Entorno OpenApi: https://apipartner.ticketbai.pro/swagger/index.html
"""

import os
import sys
import json
import hashlib
import pathlib
import pickle
import requests

URL_IDENTITY = 'https://login.consulpyme.com/connect/token'
URL_TICKETBAI = 'https://apipartner.ticketbai.pro/api'


class ResponseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def response_log(func):

    def wrapper(obj, *args, **kwargs):
        if hasattr(obj, 'log'):
            with open(obj.log, 'a', encoding='cp1252', errors='replace') as f:
                djson = json.dumps(args[3], ensure_ascii=False, indent=4, sort_keys=True) if args[3] else None
                files = ','.join(args[5].keys()) if args[5] else None
                f.write(f'{args[0].upper()}: {args[1]}\n')
                f.write(f'data: {args[2]}\n')
                f.write(f'json: {djson}\n')
                f.write(f'param: {args[4]}\n')
                f.write(f'files: {files}\n')

        error, resul = func(obj, *args, **kwargs)

        if hasattr(obj, 'log'):
            with open(obj.log, 'a', encoding='cp1252', errors='replace') as f:
                if error:
                    f.write(f'{error}\n')
                else:
                    djson = json.dumps(resul, ensure_ascii=False, indent=4, sort_keys=True)
                    f.write(f'Response:{djson}\n')

        return error, resul

    return wrapper


class TicketBai:
    response = None
    status_code = None

    def __init__(self, cwd=None, usuario=None, clave=None, log=None):
        self.error401 = False
        self.log = log
        if usuario and clave:
            self.client_id = usuario
            self.client_secret = clave
        else:
            path = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]
            path = cwd or os.path.split(path)[0]
            self.client_id, self.client_secret = self._get_config(path)

        self.token, self.token_type = self.get_token_type()

    @staticmethod
    def _get_config(path):
        fic = os.path.join(path, 'config.json')
        with open(fic, 'rb') as f:
            data = json.load(f)
        return data.get('client_id'), data.get('client_secret')

    @staticmethod
    def _get_home_config():
        home = pathlib.Path.home()
        nombre = os.path.basename(__file__).split('.')[0]
        fichero = os.path.join(home, f'.{nombre}')
        return fichero

    def token(self):
        try:
            tokens = self._get_tokens_local()
            md5 = self._get_md5()
            return tokens[md5]
        except:
            return self._get_token_identity()

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
            str_error = f'ERROR (get_token)= {response.status_code} {response.reason}:{error}'
            raise Exception(str_error)

    @response_log
    def _response(self, tipo, url, param_data=None, param_json=None, param_params=None, files=None):
        headers = {
            # 'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'{self.token_type} {self.token}'
        }

        if tipo == 'get':
            response = requests.get(url, headers=headers, params=param_params)
        elif tipo == 'post':
            response = requests.post(url, headers=headers, params=param_params, data=param_data, json=param_json, files=files)
        elif tipo == 'put':
            response = requests.put(url, headers=headers, params=param_params, data=param_data, json=param_json)
        else:
            return f'ERROR=Tipo no definido: {tipo}', None

        self.response = response
        self.status_code = response.status_code
        if 200 <= response.status_code <= 299:
            return None, json.loads(response.text or '{}')
        elif response.status_code == 401 and not self.error401:
            self.error401 = True
            self.token, self.token_type = self._get_token_identity()
            self.set_token_type(self.token, self.token_type)
            return self._response(tipo, url, param_data, param_json, param_params, files)
        else:
            str_error = f'ERROR({url})= {response.status_code}:{response.reason}{response.text}'
            return str_error, None

    def send(self, modo, funcion, param_url=None, param_data=None, param_json=None, param_params=None, files=None):
        url = f'{URL_TICKETBAI}/{funcion}'
        if param_url:
            url += '/' + '/'.join(param_url)

        error, resul = self._response(modo, url, param_data, param_json, param_params, files)
        if error:
            raise ResponseError(error)

        return resul

