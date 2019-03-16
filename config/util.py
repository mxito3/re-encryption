import ast

#这里是一些类型之间的转化
def bytesTostring(rawBytes:bytes):
    return "".join(map(chr, rawBytes))

def floatToString(rawFloatNumber:float):
    return str(int(rawFloatNumber))

def stringToBytes(rawString:str):
    return rawString.encode()

def stringToList(rawString:str):
    return ast.literal_eval(rawString)
