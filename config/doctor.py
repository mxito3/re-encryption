from umbral import pre, keys, signing
import json
import time
from . import ecdas
class Doctor(object):
    '''
        pkd：doctor的公钥
        patient_public_key:病人的公钥
        doctor_sign_key: doctor用来ecdas签名的私钥
    '''
    def pretreatment(self,patient_public_key,pkd,doctor_sign_key):
        #消息准备
        message={}
        message["name"]='someone'
        message['symptom'] = 'headache'
        #dic to json
        messageJson = json.dumps(message)
        #json to str
        messageInBytes=str.encode(messageJson)
        #ciphertest => c0
        c0, capsule = pre.encrypt(patient_public_key,messageInBytes)
        c0_string = "".join(map(chr, c0))
        timestamp = str(int(time.time()))
        ciphertext={}
        #bytes to str
        ciphertext['c0'] =c0_string
        ciphertext['doctor_public_key'] = pkd
        ciphertext['timestamp'] = timestamp  
        cipher_checker=json.dumps(ciphertext)
        cipherHash = hash(cipher_checker)

        #获得签名
        sign= ecdas.make_transaction(doctor_sign_key,cipherHash)
        cipher={}
        cipher['cipher'] = c0_string
        cipher['sign'] =  sign
        cipher['cipherHash'] = cipherHash
        cipher['cipher_checker'] = cipher_checker
        return cipher


