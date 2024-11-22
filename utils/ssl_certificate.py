from datetime import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend


class SSLCertificate:
    def __init__(self, domain, content, key):
        self.domain = domain
        self.content = content
        self.key = key

        cert = x509.load_pem_x509_certificate(content.encode(), default_backend())
        self.not_valid_before: datetime = cert.not_valid_before_utc
        self.not_valid_after: datetime = cert.not_valid_after_utc

    def __str__(self):
        return f'{self.domain} {self.not_valid_before} {self.not_valid_after}'
