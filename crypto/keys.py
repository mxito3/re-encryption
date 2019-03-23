from . import ecdas
from config import common
from umbral import pre, keys, signing
class Key(object):
    def __init__(self):#构造函数
        self.verify_key, self.__sign_key =ecdas.generate_key() 
        self.__recrypt_private_key = keys.UmbralPrivateKey.gen_key()
        self.recrypt_public_key = self.__recrypt_private_key.get_pubkey()
        self.__reencrypto_signing_key = keys.UmbralPrivateKey.gen_key()    
        self.reencrypto_verifying_key = self.__reencrypto_signing_key.get_pubkey()
        self.__reencrypto_signer = signing.Signer(private_key=self.__reencrypto_signing_key)
    
    def get_recrpto_private_Key(self):
        return self.__recrypt_private_key

    def get_signKey(self):
        return self.__sign_key
    
    def get_recrpto_signer(self):
        return self.__reencrypto_signer
