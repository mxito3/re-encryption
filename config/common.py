import json
from crypto import ecdas
import time,os
from collections import OrderedDict
def checkHash(message,message_hash):
    if hash(message) == message_hash:
        return True
    else:
        return False

def getMessage(dataIndx):
    #消息准备
    my_path = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(my_path,"../data/patient"+str(dataIndx))
    buffer = open(filename,'r').read()
    return buffer
def getDataSize(dataIndex):
    my_path = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(my_path,"../data/patient"+str(dataIndex))
    size = os.path.getsize(filename)
    return size

    

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

def serializationDrawData(keys,values):
    print("in {} {}".format(keys,values))
    temp_result={}
    for index in range(len(keys)):
        key = keys[index]
        temp_result[key] = values[index]
    result = OrderedDict(sorted(temp_result.items()))
    # for index in result.items():
    #     print(result.items[index])
    # print(result.keys)
    x=[]
    y= []
    for key in result.keys():
        x.append(key)
    for index in range(len(result.values())):
        valu=result.get(x[index])
        y.append(valu)
    
  
    # print("{}   {}".format(x,y))
    
    return x,y