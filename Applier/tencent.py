import json
import time

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ssl.v20191205 import ssl_client, models

from Applier.base_applier import BaseApplier
from utils.auth import AUTHENTICATION
from utils.ssl_certificate import SSLCertificate
from utils.unzip import UnZip

SECRET_ID = AUTHENTICATION['tencentcloud-secret-id']
SECRET_KEY = AUTHENTICATION['tencentcloud-secret-key']


class Tencent(BaseApplier):
    def __init__(self):
        self.cred = credential.Credential(SECRET_ID, SECRET_KEY)
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "ssl.tencentcloudapi.com"

        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile
        self.client = ssl_client.SslClient(self.cred, "", self.clientProfile)

    def _apply_certificate(self, domain):
        req = models.ApplyCertificateRequest()
        params = {
            "DvAuthMethod": "DNS_AUTO",
            "DomainName": domain
        }
        req.from_json_string(json.dumps(params))
        resp = self.client.ApplyCertificate(req)
        return resp.CertificateId

    def _check_certificate_domain_verification(self, certificate_id):
        req = models.CheckCertificateDomainVerificationRequest()
        params = {
            "CertificateId": certificate_id
        }
        req.from_json_string(json.dumps(params))
        resp = self.client.CheckCertificateDomainVerification(req)
        return resp.VerificationResults[0].Issued

    def _download_certificate(self, certificate_id):
        req = models.DownloadCertificateRequest()
        params = {
            "CertificateId": certificate_id
        }
        req.from_json_string(json.dumps(params))
        resp = self.client.DownloadCertificate(req)

        assert resp.ContentType == 'application/zip'
        return resp.Content

    def apply(self, domain) -> SSLCertificate:
        domain = domain.lower()

        try:
            certificate_id = self._apply_certificate(domain)
        except Exception as e:
            raise ValueError('Failed to apply certificate for domain: ' + domain) from e

        try:
            maximum_wait_time = 60
            while not self._check_certificate_domain_verification(certificate_id):
                time.sleep(60)
                maximum_wait_time -= 1
                if maximum_wait_time == 0:
                    raise TimeoutError('Domain verification timeout')
        except TimeoutError as e:
            raise e
        except Exception as e:
            raise ValueError('Failed to verify domain for certificate: ' + certificate_id) from e

        try:
            certificate = self._download_certificate(certificate_id)
        except Exception as e:
            raise ValueError('Failed to download certificate: ' + certificate_id) from e

        try:
            unzip = UnZip(certificate)
            certificate_content = unzip.retrieve(f'{domain}.pem')
            certificate_key = unzip.retrieve(f'{domain}.key')
        except Exception as e:
            raise ValueError('Failed to unzip certificate') from e
        return SSLCertificate(domain, certificate_content, certificate_key)
