import json
from . import ecdas
import time
def checkHash(message,message_hash):
    if hash(message) == message_hash:
        return True
    else:
        return False

def getMessage():
    #消息准备
    message={}
    message["name"]='someone'
    message['symptom'] = 'headache'
    #dic to json
    messageJson = json.dumps(message)
    #json to str
    return messageJson


#级联
def combine(cipher,verifyKey):
    ciphertext={}
    ciphertext['cipher']=cipher
    ciphertext['verify_key'] = verifyKey
    ciphertext['timestamp'] = time.time()
    cipherStr=str(ciphertext)
    return cipherStr

#使用ecads对clearText签名
def sign(clearText,signKey):
    sign= ecdas.make_transaction(signKey,clearText)
    return sign


#序列化
def serialization(sign,ciphertext):
    cipher={}
    cipher['sign'] =  sign
    cipher['cipher'] = ciphertext
    return cipher
#反序列化
def deserialization(cipher:object):
    sign = cipher['sign']
    ciphertext = cipher['cipher']
    return sign,ciphertext
def checkSignValid(verify_key,message,sig):
    '''
            cipher:密文
            doctor_verify_key:verify_key
            sig:签名
    '''
    if ecdas.is_valid(verify_key,message,sig):
        return True
    else:
        return False