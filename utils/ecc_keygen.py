import binascii

import os


def generate_ecc_private_key(curve_name):
    curves = {
        # NIST / SECG
        "P-256": (
            0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
            32,
        ),
        "P-384": (
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973,
            48,
        ),
        "P-521": (
            0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
            66,
        ),

        # SECG non-NIST
        "secp256k1": (
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
            32,
        ),
    }

    if curve_name not in curves:
        raise ValueError("Nieznana lub nieobsługiwana krzywa eliptyczna")

    n, size = curves[curve_name]

    # Generowanie losowej liczby o odpowiedniej długości
    random_bytes = os.urandom(size)
    random_int = int.from_bytes(random_bytes, "big")

    # Mapowanie do zakresu ⟨1, n−1⟩
    private_key_int = (random_int % (n - 1)) + 1

    return private_key_int.to_bytes(size, "big")

key_private = generate_ecc_private_key("P-256")
print(binascii.hexlify(key_private).decode().upper())
