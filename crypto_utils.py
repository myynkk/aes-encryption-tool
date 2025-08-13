import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(input_path, output_path, password):
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        f_out.write(salt)
        f_out.write(iv)
        while True:
            chunk = f_in.read(4096)
            if not chunk:
                break
            f_out.write(encryptor.update(chunk))
        f_out.write(encryptor.finalize())

def decrypt_file(input_path, output_path, password):
    with open(input_path, "rb") as f_in:
        salt = f_in.read(16)
        iv = f_in.read(16)
        key = derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        with open(output_path, "wb") as f_out:
            while True:
                chunk = f_in.read(4096)
                if not chunk:
                    break
                f_out.write(decryptor.update(chunk))
            f_out.write(decryptor.finalize())