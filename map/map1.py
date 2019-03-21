from umbral import pre, keys, signing,config
from config.doctor import Doctor
from umbral.curve import SECP256K1
from config import ecdas,common
from config.owner import Owner
from util import type_convert
import sys,json,time


#认证时间和数据大小的关系
def verifyTime_dataSize():
  result=[]
  stage1_start_time = time.time()
  config.set_default_curve(SECP256K1)
  #新建一个doctor对象，一个owner对象
  docter = Doctor()
  owner=Owner()

  #patient重加密密钥公钥
  paint_public_key = owner.recrypt_public_key

  #第一步,医生加密数据并传输给病人
  ciphertext,capsule,stage1_finish_time = docter.pretreatment(paint_public_key)


  #第二步，owner确认信息是否正确
  cipher,stage2_finish_time=owner.confirmMessage(ciphertext,capsule)
  if not cipher:
    sys.exit(0)        #owner认为信息不对则通不过

  #第三步，医生确认签名
  sign , clear_text = common.deserialization(cipher) #对owner发过来的东西反序列化　　
  
  #doctor验证owner签名
  doctor_treat_result,stage3_finish_time = docter.treat_owner_response(sign,clear_text)
  if doctor_treat_result:
    print("病例验证成功")
  else:
    print("病例验证失败")
  time_stage1 = stage1_finish_time - stage1_start_time
  time_stage2 = stage2_finish_time - stage1_finish_time
  time_stage3 = stage3_finish_time - stage2_finish_time
  result.append(time_stage1)
  result.append(time_stage2)
  result.append(time_stage3)
  return result
if __name__ == "__main__":
    result= verifyTime_dataSize()
    print(result)


  
