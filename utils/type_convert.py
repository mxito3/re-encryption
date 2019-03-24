import ast
from umbral import pre,params,config
from umbral.curve import SECP256K1
#这里是一些类型之间的转化
def bytesTostring(rawBytes:bytes):
    return "".join(map(chr, rawBytes))

def floatToString(rawFloatNumber:float):
    return str(int(rawFloatNumber))

def stringToBytes(rawString:str):
    return rawString.encode()

def stringToList(rawString:str):
    return ast.literal_eval(rawString)

def double_process(rawDouble):
    digits=3
    return round(rawDouble,digits)

def bytes_to_capsule(capsule_bytes):
    parameters=params.UmbralParameters(SECP256K1)
    capsule=pre.Capsule.from_bytes(capsule_bytes,parameters) 
    return capsule
