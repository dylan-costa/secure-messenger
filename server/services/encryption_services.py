from server.encryption.ecc import ECCurve


def generate_ecc_domain_params():
    """Public, non-secret Diffie-Hellman domain parameters for one conversation."""

    curve = ECCurve()

    return {
        "p": curve.P,
        "a": curve.a,
        "b": curve.b,
        "gx": curve.G.x,
        "gy": curve.G.y,
    }


# Registry of conversation-scoped encryption methods that need shared, public
# domain parameters generated once per conversation. Identity-scoped methods
# (RSA, Multiprime RSA, ...) need no entry here at all: their keys are plain
# per-user public keys the server just stores and relays opaquely.
DOMAIN_PARAM_GENERATORS = {
    "ECC": generate_ecc_domain_params,
}


def get_domain_param_generator(method):
    return DOMAIN_PARAM_GENERATORS.get(method)
