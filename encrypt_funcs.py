from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
from base64 import *
from config import SALT


def encrypt(pass_to_encrypt, master_hash):
    derived_key = PBKDF2(str(master_hash), SALT).read(32)

    convert = pass_to_encrypt.encode()

    cipher = AES.new(derived_key, AES.MODE_EAX)

    nonce = cipher.nonce  # Unique to every transaction

    ciphertext, tag = cipher.encrypt_and_digest(convert)

    nonce_added = ciphertext + nonce

    encoded_ciphertext = b64encode(nonce_added).decode()

    return encoded_ciphertext


def decrypt(pass_to_dec, master_hash):
    pass_to_dec += "=" * (4 - len(pass_to_dec) % 4)

    convert = b64decode(pass_to_dec)

    key = PBKDF2(str(master_hash), SALT).read(32)

    nonce = convert[-16:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(convert[:-16])  # Excluding nonce

    return plaintext.decode()
