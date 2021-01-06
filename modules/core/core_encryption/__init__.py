from old.py_old import encryption
import os
import sys
import base64
import json
from typing import Any, Dict
from types import FunctionType

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

settings = None

# import settings
from utils import print_error, print_warning 

class EncryptionHandler:
    key: RsaKey
    cipher: PKCS1_OAEP
    key_loader_funcs: Dict[str, FunctionType]
    key_loader_info: list[dict[str, str]]

   
    def __init__(self, key_loader_info: list[dict[str, str]]):
        self.key_loader_funcs = {
            "env_var": self.load_key_from_env,
            "file": self.load_key_from_file
        }
        self.key_loader_info = key_loader_info

    
    def load_key(self, key_loader_info: list[dict[str, str]]=None):
        if key_loader_info is None:
            key_loader_info = self.key_loader_info
        
        for i in key_loader_info:
            if self.key_loader_funcs[i['type']](**i):
                self.cipher = PKCS1_OAEP.new(self.key)
                print(f"Key loaded: {i}")
                return
            else:
                print(f"Could not load key: {i}")
                
        print_error("FATAL ERROR: No privake key could be loaded.")
    
    
    def load_key_from_env(self, env_var_name="AZERO_PKEY", **kwargs) -> bool:
        key_text = os.getenv(env_var_name)
        try:
            self.key = RSA.import_key(key_text)
            return True
        except Exception as e:
            print_error(e)
            return False
            
        
    def load_key_from_file(self, filepath, **kwargs) -> bool:
        if os.path.isfile(filepath):
            key_file = open(filepath)
            self.key = RSA.import_key(key_file.read())
            key_file.close()
            return True
        
        else:
            print_error(f"File not found: {filepath}")
            return False
        
    def decrypt_with_server_key(self, message: str) -> dict:
        base64_bytes = message.encode('utf8')
        message_bytes = base64.b64decode(base64_bytes)
        
        decrypted: bytes = b"";
        
        # print(len(message_bytes))
        
        while len(message_bytes) > 0:
            batch = b"";
            
            if len(message_bytes) >= self.key.size_in_bytes():
                batch = message_bytes[:self.key.size_in_bytes()]
                # print(len(batch))
                message_bytes = message_bytes[len(batch):]
                # print(len(message_bytes))
            else:
                batch = message_bytes
                message_bytes = ""

            decrypted += self.cipher.decrypt(batch)
        return json.loads(decrypted.decode('utf8'))
    
    
    def encrypt_with_key(self, key: str, response: dict)->list[bytes]:
        response_bytes: bytes = json.dumps(response).encode("utf-8")
        encrypted: list[bytes] = [];
        
        response_key = RSA.import_key(key)
        response_cipher = PKCS1_OAEP.new(response_key)
        
        message_batch_size: int = int(response_key.size_in_bytes()/2)
        # print(f"{response_key.size_in_bytes()=}")
        
        while len(response_bytes) > 0:
            batch = b"";
            
            if len(response_bytes) >= message_batch_size:
                batch = response_bytes[:message_batch_size]
                # print(f"{len(batch)=}")
                response_bytes = response_bytes[len(batch):]
                # print(f"{len(response_bytes)=}")
            else:
                batch = response_bytes
                response_bytes = ""

            encrypted.append(base64.b64encode(response_cipher.encrypt(batch)).decode("utf8"))
            
        # print(encrypted)
        return encrypted

e_handler: EncryptionHandler = None

def init(name: str, path: str, args: dict[str, Any]):
    global e_handler
    e_handler = EncryptionHandler(args["key-loaders"])
    e_handler.load_key()


def decrypt_with_server_key(message) -> dict:
    global e_handler    
    return e_handler.decrypt_with_server_key(message)


def encrypt_with_key(key: str, response: dict) -> dict:
    global e_handler    
    return e_handler.encrypt_with_key(key, response)