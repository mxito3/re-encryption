from utils.crypto import Crypto as cryptoUtil
from crypto import ecdas
class User(object):
    def __init__(self):
        self.verify_key, self.__sign_key =ecdas.generate_key() 
    def signup(self):
        return cryptoUtil.generateId(self.verify_key)
        