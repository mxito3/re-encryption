from umbral import pre, keys, signing
import json
import time
from crypto import ecdas
from config import common
from utils import type_convert
from crypto.keys import Key
class Doctor(object):
    def __init__(self):#构造函数
        self.keys = Key()
    def pretreatment(self,patient_public_key,data):
        #获取病例
        # messageInBytes=str.encode(data) #转成bytes形式
        #重加密
        c0, capsule = pre.encrypt(patient_public_key,data)
        #级联
        ciphertext=common.combine(c0,self.keys.verify_key.to_string())
        #求hash值
        cipher_hash = hash(ciphertext)
        #对hash值结果获得签名
        sign=common.sign(cipher_hash,self.keys.get_signKey())
        #发送给owner之前先序列化
        cipher=common.serialization(sign,ciphertext)
        
        finishtime = time.time()
        return cipher,capsule,finishtime

    def treat_owner_response(self,sign,ciphertext):

        #获得密文
        cipher = type_convert.stringToList(ciphertext)
        #求hash
        cipher_hash = hash(str(ciphertext))
        #获得owner的acads公钥
        verify_key = cipher['verify_key']
        #验证签名
        if common.checkSignValid(verify_key,cipher_hash,sign):
            finishtime = time.time()
            return True,finishtime
        else:
            finishtime = time.time()
            return False,finishtime

