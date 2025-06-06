def xor_encrypt(text: str, key: str) -> bytes:
    text_bytes = text.encode("utf-8")
    key_bytes = key.encode("utf-8")
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])

def xor_decrypt(data: bytes, key: str) -> str:
    key_bytes = key.encode("utf-8")
    decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])
    return decrypted.decode("utf-8")
