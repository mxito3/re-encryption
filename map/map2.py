#coding:utf-8
import common_operate ,json,time
from crypto.recrypto import RecryptoUtil
from config.doctor import Doctor
from umbral.curve import SECP256K1
from config import ecdas,common
from config.owner import Owner
import matplotlib.pyplot as plt
from matplotlib.font_manager import  *

need_test_file = 10
def init():
  config.set_default_curve(SECP256K1)

def encryptoTime_dataSize():
  result=[]
  for index in range(common_operate.need_test_file):
      perResult = encrypto_per_file(index)
      result.append(perResult)
  print(result)

def encrypto_per_file(owner_id):
  #新建一个doctor对象，一个owner对象
    doctor = Doctor()
    owner=Owner(owner_id)
    recrypto_util = RecryptoUtil(doctor.recrypt_public_key ,doctor.get_recrpto_private_Key,doctor.get_signKey(),doctor.verify_key,owner.recrypt_public_key,owner.get_recrpto_private_Key)
    ciphertext,capsule,time_used = recrypto_util.encrypto(owner.message)
    return time_used

encryptoTime_dataSize()