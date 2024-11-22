from Applier.tencent import Tencent
from Deployer.qiniu_ import Qiniu


class CertBuddy:
    def __init__(self):
        self.applier = Tencent()
        self.deployer = Qiniu()

        self.joblist = self.get_joblist()

    @staticmethod
    def get_joblist():
        with open('.joblist') as f:
            job_data = f.read()
        return job_data.strip().split('\n')

    def run(self):
        for domain in self.joblist:
            try:
                print(f'Processing {domain}')
                print('Applying certificate...')
                certificate = self.applier.apply(domain)
                print('Uploading certificate...')
                self.deployer.deploy(certificate)
            except Exception as e:
                print(f'Failed to process {domain}: {e}')


cb = CertBuddy()
cb.run()
