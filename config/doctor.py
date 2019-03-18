from umbral import pre, keys, signing
import json
import time
from . import ecdas,common,util
class Doctor(object):
    '''
        verify_key：ecads验证的公钥 
        __sign_key: doctor用来ecdas签名的私钥
    '''
    def __init__(self):#构造函数
        self.verify_key, self.__sign_key =ecdas.generate_key() 
  
    def get_signKey(self):
        return self.__sign_key

    def pretreatment(self,patient_public_key):
        #获取病例
        messageJson=common.getMessage() #读取病例
        messageInBytes=str.encode(messageJson) #转成bytes形式
        #重加密
        c0, capsule = pre.encrypt(patient_public_key,messageInBytes)
        #级联
        ciphertext=common.combine(c0,self.verify_key.to_string())
        #求hash值
        cipher_hash = hash(ciphertext)
        #对hash值结果获得签名
        sign=common.sign(cipher_hash,self.__sign_key)
        #发送给owner之前先序列化
        cipher=common.serialization(sign,ciphertext)
        
        return cipher,capsule

    def treat_owner_response(self,sign,ciphertext):

        #获得密文
        cipher = util.stringToList(ciphertext)
        #求hash
        cipher_hash = hash(str(ciphertext))
        #获得owner的acads公钥
        verify_key = cipher['verify_key']
        #验证签名
        if common.checkSignValid(verify_key,cipher_hash,sign):
            return True
        else:
            return False

