from __future__ import print_function, division, absolute_import
import json
import time
from hashlib import sha1
try:
    from urllib2 import urlopen, Request, HTTPError, URLError
except ImportError:
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError


class GuYuJieZi(object):
    class Options(object):
        font_name = None
        font_formats = ['woff2', 'woff', 'eot', 'otf/ttf']

    URL_ENCRYPT = 'https://guyujiezi.com/api/encrypt'
    URL_NONCE = 'https://guyujiezi.com/api/nonce'
    AUTH_TYPE = 'GYJZ'

    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        self._last_error = None

    def _authorize(self):
        nonce = '%f' % time.time()
        signature = sha1(':'.join((self.public_key, self.secret_key, nonce)).encode()).hexdigest()
        return '{type} pk={pk}, nonce={nonce}, sign={sign}'.format(
            type=self.AUTH_TYPE,
            pk=self.public_key,
            nonce=nonce,
            sign=signature
        )

    def _request(self, *args, **kwargs):
        def jsonify(response):
            try:
                return json.loads(response.read().decode('utf8'))
            except:
                raise RuntimeError('Unexpected response')

        try:
            response = urlopen(*args, **kwargs)
            payload = jsonify(response)
            response.close()
            return True, payload
        except HTTPError as e:
            if e.code >= 500:
                raise RuntimeError('Service unavailable')
            elif e.code >= 400:
                return False, jsonify(e)
            raise RuntimeError('Unexpected response')
        except URLError:
            raise RuntimeError('Service unavailable')

    def encrypt(self, plaintext, shadowtext, options=None):
        data = {
            'plaintext': plaintext,
            'shadowtext': shadowtext,
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self._authorize(),
        }
        request = Request(self.URL_ENCRYPT, json.dumps(data).encode(), headers, method='POST')
        success, payload = self._request(request)

        if not success:
            self._last_error = payload
            return False
        
        return payload

    @property
    def last_error(self):
        return self._last_error

    def nonce(self):
        success, payload = self._request(self.URL_NONCE)

        if not success:
            self._last_error = payload
            return False

        return payload.get('nonce')

        
