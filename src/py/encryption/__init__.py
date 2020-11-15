import os
import sys
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class EncryptionHandler:
    key: RSA
    cipher: PKCS1_OAEP
    
    def __init__():
        pass