from umbral import pre, keys, signing,config
from config.doctor import Doctor
from umbral.curve import SECP256K1
from config import ecdas,util,common
from config.owner import Owner
import sys,json
if __name__ == "__main__":

  #设置默认的加密算法
  config.set_default_curve(SECP256K1)

  #新建一个doctor对象，一个owner对象
  docter = Doctor()
  owner=Owner()

  #patient重加密密钥公钥
  paint_public_key = owner.recrypt_public_key

  #第一步,医生加密数据并传输给病人
  ciphertext,capsule = docter.pretreatment(paint_public_key)


  #第二步，owner确认信息是否正确
  cipher=owner.confirmMessage(ciphertext,capsule)
  if not cipher:
    sys.exit(0)        #owner认为信息不对则通不过

  #第三步，医生确认签名
  sign , clear_text = common.deserialization(cipher) #对owner发过来的东西反序列化　　
  
  #doctor验证owner签名
  doctor_treat_result = docter.treat_owner_response(sign,clear_text)
  if doctor_treat_result:
    print("病例验证成功")
  else:
    print("病例验证失败")
