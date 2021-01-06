from . import AZeroModuleWrapper

class EncryptionWrapper(AZeroModuleWrapper):
    module_type = "encryption"
    required_attrs = [
        'decrypt_with_server_key',
        # 'encrypt_with_id_key'
    ]

    
    def decrypt_with_server_key(self, message) -> dict:
        return self.loaded.decrypt_with_server_key(message)
    

    def encrypt_with_key(self, key: str, response: str) -> list[bytes]:
        return self.loaded.encrypt_with_key(key, response)