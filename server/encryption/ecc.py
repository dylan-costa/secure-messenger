from typing import cast
from random import randint

from sympy import randprime
from tinyec import ec
from tinyec.ec import Point


class ECCurve:

    def __init__(self):

        # Generate P

        self.P = cast(
            int,
            randprime(1000, 10000)
        )

        # Generate a and b

        while True:

            self.a = randint(
                1,
                self.P - 1
            )

            self.b = randint(
                1,
                self.P - 1
            )

            if (
                4 * self.a**3
                + 27 * self.b**2
            ) % self.P != 0:

                break

        # Find a point G on the curve

        while True:

            x = randint(
                1,
                self.P - 1
            )

            z = (
                x**3
                + self.a * x
                + self.b
            ) % self.P

            for y in range(self.P):

                if (
                    y**2
                ) % self.P == z:

                    G = (x, y)

                    break

            else:

                continue

            break

        # Create subgroup

        field = ec.SubGroup(
            self.P,
            G,
            self.P,
            1
        )

        # Create elliptic curve

        self.curve = ec.Curve(
            self.a,
            self.b,
            field
        )

        # Create base point

        self.G = ec.Point(
            self.curve,
            G[0],
            G[1]
        )


class ECC:

    def __init__(
        self,
        curve
    ):

        self.curve = curve

        self.private_key = None
        self.public_key = None

        self.shared_point = None
        self.shared_secret = None

    def generate_keys(self):

        # Choose private key

        self.private_key = randint(
            1,
            self.curve.P - 1
        )

        # Calculate public key

        self.public_key = cast(
            Point,
            self.curve.G
            * self.private_key
        )

        return self.public_key

    def generate_shared_secret(
        self,
        other_public_key
    ):

        if self.private_key is None:

            raise ValueError(
                "Private key has not been generated."
            )

        # Calculate:

        # S = private_key * other_public_key

        self.shared_point = cast(
            Point,
            other_public_key
            * self.private_key
        )

        # Use x-coordinate as secret

        self.shared_secret = (
            self.shared_point.x
            % 256
        )

        return self.shared_secret

    def encrypt(
        self,
        message
    ):

        if self.shared_secret is None:

            raise ValueError(
                "Shared secret has not been generated."
            )

        message_bytes = message.encode()

        encrypted_message = bytes(
            byte ^ self.shared_secret
            for byte in message_bytes
        )

        return encrypted_message

    def decrypt(
        self,
        encrypted_message
    ):

        if self.shared_secret is None:

            raise ValueError(
                "Shared secret has not been generated."
            )

        decrypted_message = bytes(
            byte ^ self.shared_secret
            for byte in encrypted_message
        )

        return decrypted_message.decode()


if __name__ == "__main__":

    # Create one shared elliptic curve

    curve = ECCurve()

    # Create Alice and Bob

    alice = ECC(curve)
    bob = ECC(curve)

    # Generate keys

    alice.generate_keys()
    bob.generate_keys()

    # Exchange public keys

    alice.generate_shared_secret(
        bob.public_key
    )

    bob.generate_shared_secret(
        alice.public_key
    )

    # Verify shared secret

    print(
        "Shared secrets match:"
    )

    print(
        alice.shared_secret
        == bob.shared_secret
    )

    # Encrypt message

    message = "Hello Bob"

    encrypted_message = alice.encrypt(
        message
    )

    print(
        "\nEncrypted message:"
    )

    print(
        encrypted_message
    )

    # Bob decrypts

    decrypted_message = bob.decrypt(
        encrypted_message
    )

    print(
        "\nDecrypted message:"
    )

    print(
        decrypted_message
    )

    print(
        "\nMessages match:"
    )

    print(
        message
        == decrypted_message
    )