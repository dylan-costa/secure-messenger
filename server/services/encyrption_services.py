from server.encryption.rsa import RSA
from server.encryption.ecc import ECC, ECCurve


class EncryptionService:

    def __init__(self, method):

        self.method = method
        self.encryption = None

    def initialize(self):

        if self.method == "RSA":

            self.encryption = RSA()

        elif self.method == "ECC":

            curve = ECCurve()

            self.encryption = ECC(curve)

        else:

            raise ValueError(
                "Unsupported encryption method."
            )