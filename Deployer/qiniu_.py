import hashlib

import qiniu
import requests

from Deployer.base_deployer import BaseDeployer
from utils.auth import AUTHENTICATION
from utils.ssl_certificate import SSLCertificate


ACCESS_KEY = AUTHENTICATION['qiniu-access-key']
SECRET_KEY = AUTHENTICATION['qiniu-secret-key']


class Qiniu(BaseDeployer):
    CODE_OK = 200

    def __init__(self):
        self.auth = qiniu.Auth(ACCESS_KEY, SECRET_KEY)

    def _method(self, method, uri, data):
        token = self.auth.token_of_request(uri)
        headers = {
            'Authorization': f'QBox {token}',
            'Content-Type': 'application/json'
        }
        url = 'https://api.qiniu.com' + uri
        with method(url, headers=headers, json=data) as resp:
            return resp.json()

    def _get(self, uri):
        return self._method(requests.get, uri, None)

    def _post(self, uri, data):
        return self._method(requests.post, uri, data)

    def _put(self, uri, data):
        return self._method(requests.put, uri, data)

    def _get_certificate_list(self, marker, limit):
        uri = '/sslcert?marker={}&limit={}'.format(marker, limit)
        return self._get(uri)

    def _upload_certificate(self, certificate: SSLCertificate):
        uri = '/sslcert'
        certificate_string = certificate.domain + '$' + certificate.not_valid_after.strftime('%Y-%m-%d %H:%M:%S')
        sign = 'AUTO$' + hashlib.md5(certificate_string.encode()).hexdigest()[:6]
        data = {
            'name': sign,
            'pri': certificate.key,
            'ca': certificate.content,
        }
        return self._post(uri, data)['certID']

    def _get_certificate(self, certificate_id):
        uri = '/sslcert/{}'.format(certificate_id)
        return self._get(uri)

    def _deploy_certificate(self, certificate: SSLCertificate, certificate_id: str):
        uri = '/domain/{}/httpsconf'.format(certificate.domain)
        data = {
            'certId': certificate_id,
            'forceHttps': True,
        }
        resp = self._put(uri, data)
        return resp

    def deploy(self, certificate: SSLCertificate):
        try:
            certificate_id = self._upload_certificate(certificate)
        except Exception as e:
            raise ValueError('Failed to upload certificate') from e
        try:
            assert self._deploy_certificate(certificate, certificate_id)['code'] == self.CODE_OK
        except Exception as e:
            print(e)
            raise ValueError('Failed to deploy certificate') from e
