from . import ecdas
from umbral import pre, keys, signing,config
class Owner(object):
    '''
        cipher:医生传过来的信息
    '''
    def __init__(self):
        self.recrypt_private_key = keys.UmbralPrivateKey.gen_key()
        self.recrypt_public_key = self.recrypt_private_key.get_pubkey()
    
    def checkValid(cipher,doctor_verify_key,message,sig):

        '''
            cipher:密文
            doctor_verify_key:verify_key
            sig:签名
        '''
        if ecdas.is_valid(doctor_verify_key,message,sig):
            return True
        else:
            return False