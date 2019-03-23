from crypto import ecdas
from config import common
from umbral import pre, keys, signing,config
from utils import type_convert
import time
from crypto.keys import Key
class Owner(object):
    '''
        verify_key：ecads验证的公钥 
        __sign_key: owner用来ecdas签名的私钥
        message: 自己的简历信息
        __recrypt_private_key：重加密私钥
        recrypt_public_key：重加密公钥
    '''
    def __init__(self,id):
        self.keys = Key()
        self.message = type_convert.stringToBytes(common.getMessage(id))

    def checkMessage(self,ciphertext,capsule):
        cleartext = pre.decrypt(ciphertext=ciphertext,
                        capsule=capsule,
                        decrypting_key=self.keys.get_recrpto_private_Key())
        if(cleartext == self.message):
            return True
        else:
            return False

    #确认病例是否正确
    def confirmMessage(self,ciphertext,capsule):
        #获得签名
        sign=ciphertext.get('sign')
        #获得密文
        cipher= type_convert.stringToList(ciphertext['cipher'])
        #获得doctor的ecads公钥
        doctor_verify_key= cipher['verify_key']
        #验证doctor签名
        cipher_hash = hash(str(cipher))
        verifyResult=common.checkSignValid(doctor_verify_key,cipher_hash,sign)
        if not verifyResult:
            print("医生签名验证失败")
            return None
        print("医生签名验证成功")

        #查看病例是否是自己的，是否信息正确
        c0=cipher['cipher']

        #用重加密私钥解密之后判断是不是自己的病例
        if not self.checkMessage(c0,capsule):
            print("病例不是owner自己的")
            return None
        else:   #信息正确
            print("病例是owner自己的")

        #准备回复doctor

        #级联
        c1=common.combine(ciphertext,self.keys.verify_key.to_string())
        
        #求hash
        cipher_hash = hash(str(c1))
        #签名
        sign=common.sign(cipher_hash,self.keys.get_signKey())
        finishtime = time.time()
        return common.serialization(sign,c1),finishtime

