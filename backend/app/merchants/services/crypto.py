import secrets

from ..schemas import KeysPair


def generate_tokens() -> KeysPair:
    public_key = secrets.token_hex(20)
    private_key = secrets.token_hex(40)
    return KeysPair(public_key=public_key, private_key=private_key)
