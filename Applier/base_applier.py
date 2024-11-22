from utils.ssl_certificate import SSLCertificate


class BaseApplier:
    def apply(self, domain) -> SSLCertificate:
        raise NotImplementedError
