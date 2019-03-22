# coding:utf-8
import common_operate
import json
import time
from crypto.recrypto import RecryptoUtil
from config.doctor import Doctor
from umbral.curve import SECP256K1
from config import ecdas, common
from config.owner import Owner
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
from util import type_convert


def init():
    config.set_default_curve(SECP256K1)


def encryptoTime_dataSize():
    result = []
    for index in range(common_operate.need_test_file):
        perResult = encrypto_per_file(index)
        result.append(type_convert.double_process(perResult))
    print(result)
    title=u'病例加密时间与病例大小的关系'
    xlable=u'病例大小(字节)'
    ylable=u'病例加密时间'
    draw_map(title,xlable,ylable,result)

def draw_map(title,xlable,ylable,y):
    x,y = common.serializationDrawData(dataSize,y)
    myfont = common_operate.get_font()
    print('{},{}'.format(x,y))
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.plot(x,y,color='red',label='data decrypto',marker='o')
    plt.title(title,fontproperties=myfont)
    plt.xlabel(xlable,fontproperties=myfont)
    plt.ylabel(ylable,fontproperties=myfont)
    plt.legend()
    plt.show()

def encrypto_per_file(owner_id):
    # 新建一个doctor对象，一个owner对象
    doctor = Doctor()
    owner = Owner(owner_id)
    test = RecryptoUtil()
    ciphertext,capsule,time_used=test.encrypto(owner.message,doctor.keys.recrypt_public_key)
    kfrags,timeUsed1=test.approve(doctor.keys.get_recrpto_private_Key(),doctor.keys.get_recrpto_signer(),owner.keys.recrypt_public_key)
    cfrags = test.re_encrypto(capsule,kfrags,doctor.keys.recrypt_public_key,owner.keys.recrypt_public_key,doctor.keys.reencrypto_verifying_key)
    result = test.decrypt(cfrags,capsule,owner.message,ciphertext, owner.keys.get_recrpto_private_Key())
    print(result)
    return time_used


if __name__ == "__main__":
    dataSize =common_operate.getDataSize()
    encryptoTime_dataSize()
