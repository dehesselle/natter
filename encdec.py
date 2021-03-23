# SPDX-License-Identifier: MIT
# https://github.com/dehesselle/natter

################################################################################
#
#      *** You should tread carefully whenever you're about to use
#          somebody else's code that does something with encryption! ***
#
# Inspired by
# https://nitratine.net/blog/post/encryption-and-decryption-in-python
# I think I'm doing ok here, but I'm neither a security expert nor do I have
# to protect state secrets with my code.
#
#                       *** You have been warned! ***
#
################################################################################

# What this code is supposed to do:
#   - generate a (randomly) salted encryption key from a user-given password
#   - use that key to encrypt a piece of text
#   - prepend the salt to the encrypted result so that the key can be 
#     regenerated later (together with the correct password of course)
#     for decryption
#
# Intended usage is to have a way to not store e.g. credentials in clear
# text to configurations files etc.


from base64 import b64decode, b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from os import urandom


def generate_key(password: str, salt: bytes) -> str:
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return b64encode(kdf.derive(password))


def encrypt(cleartext: str, password: str) -> str:
    salt = urandom(16)
    fernet = Fernet(generate_key(password, salt))
    return (b64encode(salt)[0:22] + b64encode(fernet.encrypt(cleartext.encode()))).decode("UTF-8")


def decrypt(crypttext: str, password: str) -> str:
    salt = b64decode((crypttext[0:22] + "==").encode())
    crypttext = crypttext[22:]  # remove salt
    fernet = Fernet(generate_key(password, salt))
    return fernet.decrypt(b64decode(crypttext.encode())).decode("UTF-8")
