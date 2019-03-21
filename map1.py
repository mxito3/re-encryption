#coding:utf-8
from umbral import pre, keys, signing,config
from config.doctor import Doctor
from umbral.curve import SECP256K1
from config import ecdas,common
from config.owner import Owner
from util import type_convert
import sys,json,time
import matplotlib.pyplot as plt

from matplotlib.font_manager import  *
need_test_file = 10
#认证时间和数据大小的关系
def verifyTime_dataSize():
  result=[]
  stage1Time=[]
  stage2Time=[]
  stage3Time=[]
  dataSize = getDataSize()
  config.set_default_curve(SECP256K1)
  for index in range(need_test_file):
    perResult = verify(index)
    result.append(perResult)
 

  for index in range(len(result)):
    stage1Time.append(result[index][0])
    stage2Time.append(result[index][1])
    stage3Time.append(result[index][2])
  
  timeUsed=[]
  timeUsed.append(stage1Time)
  timeUsed.append(stage2Time)
  timeUsed.append(stage3Time)
  drawMap(dataSize,timeUsed)

def getDataSize():
  result=[]
  for index in range(need_test_file):
    perSize= common.getDataSize(index)
    result.append(perSize)
  return result


def verify(owner_id):
  result=[]
  #新建一个doctor对象，一个owner对象
  stage1_start_time = time.time()
  docter = Doctor()
  owner=Owner(owner_id)

  #patient重加密密钥公钥
  paint_public_key = owner.recrypt_public_key

  #第一步,医生加密数据并传输给病人
  ciphertext,capsule,stage1_finish_time = docter.pretreatment(paint_public_key,owner_id)


  #第二步，owner确认信息是否正确
  cipher,stage2_finish_time=owner.confirmMessage(ciphertext,capsule)
  if not cipher:
    sys.exit(0)        #owner认为信息不对则通不过

  #第三步，医生确认签名
  sign , clear_text = common.deserialization(cipher) #对owner发过来的东西反序列化　　
  
  #doctor验证owner签名
  doctor_treat_result,stage3_finish_time = docter.treat_owner_response(sign,clear_text)
  if doctor_treat_result:
    print("patient{}病例验证成功".format(str(owner_id)))
  else:
    print("patient{}病例验证失败".format(str(owner_id)))
  digits=3
  time_stage1 = round(stage1_finish_time - stage1_start_time,digits)
  time_stage2 = round(stage2_finish_time - stage1_finish_time,digits)
  time_stage3 = round(stage3_finish_time - stage2_finish_time,digits)
  result.append(time_stage1)
  result.append(time_stage2)
  result.append(time_stage3)
  return result

def drawMap(datasize,timeUsed):
  print(datasize)

  myfont = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
  plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
  
  stage1Time=timeUsed[0] 
  stage2Time=timeUsed[1]
  stage3Time=timeUsed[2]
  stage1_x,stage1_y=common.serializationDrawData(datasize,stage1Time)
  print("x{}\n y{}".format(stage1_x,stage1_y))
  stage2_x,stage2_y=common.serializationDrawData(datasize,stage2Time)
  print("x{}\n y{}".format(stage2_x,stage2_y))
  stage3_x,stage3_y=common.serializationDrawData(datasize,stage3Time)
  print("x{}\n y{}".format(stage3_x,stage3_y))
  
  
  
  plt.plot(stage1_x,stage1_y,color='red',label='stage 1')
  plt.plot(stage2_x,stage2_y,color='blue',label='stage 2')
  plt.plot(stage3_x,stage3_y,color='green',label='stage 3')
  plt.title(u'病例处理时间与病例大小的关系',fontproperties=myfont)
  plt.xlabel(u'病例大小(字节)',fontproperties=myfont)
  plt.ylabel(u'加密需要的时间',fontproperties=myfont)
  plt.legend()
  plt.show()

if __name__ == "__main__":
    result= verifyTime_dataSize()
  


  
