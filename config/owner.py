from . import ecdas,common
from umbral import pre, keys, signing,config
from util import type_convert
class Owner(object):
    '''
        verify_key：ecads验证的公钥 
        __sign_key: owner用来ecdas签名的私钥
        message: 自己的简历信息
        __recrypt_private_key：重加密私钥
        recrypt_public_key：重加密公钥
    '''
    def __init__(self):
        self.__recrypt_private_key = keys.UmbralPrivateKey.gen_key()
        self.recrypt_public_key = self.__recrypt_private_key.get_pubkey()
        self.message = common.getMessage()
        self.verify_key, self.__sign_key =ecdas.generate_key() 
  
    def get_signKey(self):
        return self.__sign_key

    def checkMessage(self,ciphertext,capsule):
        cleartext = pre.decrypt(ciphertext=ciphertext,
                        capsule=capsule,
                        decrypting_key=self.__recrypt_private_key)
        if(type_convert.bytesTostring(cleartext) == self.message):
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
        c1=common.combine(ciphertext,self.verify_key.to_string())
        
        #求hash
        cipher_hash = hash(str(c1))
        #签名
        sign=common.sign(cipher_hash,self.__sign_key)
        
        return common.serialization(sign,c1)

