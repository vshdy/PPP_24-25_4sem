import base64
from app.services.huffman import huffman_encode, huffman_decode
from app.services.xor import xor_encrypt, xor_decrypt

def encrypt_and_encode(text: str, key: str) -> dict:

    xor_data = xor_encrypt(text, key)
    base64_str = base64.b64encode(xor_data).decode("utf-8")

    encoded, codes = huffman_encode(base64_str)
    padding = (8 - len(encoded) % 8) % 8

    return {
        "encoded_data": encoded,
        "huffman_codes": codes,
        "padding": padding
    }

def decode_and_decrypt(payload: dict) -> str:
    decoded_base64 = huffman_decode(
        payload["encoded_data"],
        payload["huffman_codes"]
    )

    padding = payload.get("padding", 0)
    if padding:
        decoded_base64 += "=" * padding

    decoded_bytes = base64.b64decode(decoded_base64)
    return xor_decrypt(decoded_bytes, payload["key"])


