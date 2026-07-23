from math import gcd
from Crypto.Util import number


class RSA:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_keys(self):
        """
        Generate an educational RSA key pair.

        Returns:
            public_key: (e, n)
            private_key: (d, n)
        """

        # Generate two prime numbers
        p = number.getPrime(512)
        q = number.getPrime(512)

        # Calculate n
        n = p * q

        # Calculate Euler's totient
        tn = (p - 1) * (q - 1)

        # Choose the public exponent e
        e = 65537

        # Make sure e and tn are relatively prime
        while gcd(e, tn) != 1:
            e += 2

        # Calculate the private exponent d
        d = pow(e, -1, tn)

        self.public_key = (e, n)
        self.private_key = (d, n)

        return self.public_key, self.private_key

    def message_to_integer(self, message):
        """
        Convert a text message into an integer.
        """

        message_number = "".join(
            str(ord(char)).zfill(3)
            for char in message
        )

        return int(message_number)

    def integer_to_message(self, message_number):
        """
        Convert an integer back into a text message.
        """

        message_string = str(message_number)

        # Ensure the string has groups of 3 digits
        if len(message_string) % 3 != 0:
            message_string = message_string.zfill(
                ((len(message_string) // 3) + 1) * 3
            )

        chunks = [
            message_string[i:i + 3]
            for i in range(0, len(message_string), 3)
        ]

        return "".join(
            chr(int(chunk))
            for chunk in chunks
        )

    def encrypt(self, message, public_key=None):
        """
        Encrypt a message using:

        C = M^e mod n
        """

        if public_key is None:
            public_key = self.public_key

        if public_key is None:
            raise ValueError("Keys have not been generated.")

        e, n = public_key

        M = self.message_to_integer(message)

        if M >= n:
            raise ValueError(
                "Message is too large for this RSA key."
            )

        C = pow(M, e, n)

        return C

    def decrypt(self, ciphertext, private_key=None):
        """
        Decrypt a message using:

        M = C^d mod n
        """

        if private_key is None:
            private_key = self.private_key

        if private_key is None:
            raise ValueError("Keys have not been generated.")

        d, n = private_key

        M = pow(ciphertext, d, n)

        return self.integer_to_message(M)


if __name__ == "__main__":

    rsa = RSA()

    public_key, private_key = rsa.generate_keys()

    message = "Hello Bob"

    print("Original message:")
    print(message)

    encrypted_message = rsa.encrypt(
        message,
        public_key
    )

    print("\nEncrypted message:")
    print(encrypted_message)

    decrypted_message = rsa.decrypt(
        encrypted_message,
        private_key
    )

    print("\nDecrypted message:")
    print(decrypted_message)