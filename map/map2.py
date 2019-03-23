# coding:utf-8
import common_operate
import json
import time
from crypto.recrypto import RecryptoUtil
from user.doctor import Doctor
from umbral.curve import SECP256K1
from crypto import ecdas
from config import common
from user.owner import Owner
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
from utils import type_convert
import threading
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def init():
    config.set_default_curve(SECP256K1)


def encryptoTime_dataSize(data_size):
    encrypto = []
    approve = []
    re_encrypto = []
    decrypto = []
    for index in range(common_operate.need_test_file):
        perResult = encrypto_per_file(index)
        encrypto.append(perResult[0])
        approve.append(perResult[1])
        re_encrypto.append(perResult[2])
        decrypto.append(perResult[3])
    draw_map_all(encrypto, approve, re_encrypto, decrypto,data_size)


def draw_map_all(encrypto, approve, re_encrypto, decrypto,data_size):
    x=data_size
    map1 = draw_parament_serialization(u'医生授权时间与病例大小的关系',u'病例大小(字节)',u'病例授权时间(s)',u'case approve time',[0,0.02])
    map2 = draw_parament_serialization(u'重加密时间与病例大小的关系',u'病例大小(字节)',u'病例重加密时间(s)',u'case re_encrypto time',[0.01,0.02])
    map3 = draw_parament_serialization(u'解密时间与病例大小的关系',u'病例大小(字节)',u'病例解密时间(s)',u'case decrypto time',[0.02,0.1])
    map4 = draw_parament_serialization(u'加密时间与病例大小的关系',u'病例大小(字节)',u'病例加密时间(s)',u'case encrypto time',[0,0.01])
    # threading.Thread(target=draw_map, args=(
    #     map1['title'], map1['xlable'], map1['ylable'], map1['line_lable'], map1['y_lim'],x,approve)).start()
    # threading.Thread(target=draw_map, args=(
    #     map2['title'], map2['xlable'], map2['ylable'], map2['line_lable'],map2['y_lim'],x,re_encrypto)).start()
    # threading.Thread(target=draw_map, args=(
    #     map3['title'], map3['xlable'], map3['ylable'], map3['line_lable'], map3['y_lim'],x,decrypto)).start()
    threading.Thread(target=draw_map, args=(
        map4['title'], map4['xlable'], map4['ylable'], map4['line_lable'],map4['y_lim'], x,encrypto)).start()


def draw_map(title, xlable, ylable, line_lable,ylim,x,y):
    axes = plt.gca()
    axes.set_ylim(ylim)
    x, y = common.serializationDrawData(x, y)
    myfont = common_operate.get_font()
    print('{},{}'.format(x, y))
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.plot(x, y, color='red', label=line_lable, marker='o')
    plt.title(title, fontproperties=myfont)
    plt.xlabel(xlable, fontproperties=myfont)
    plt.ylabel(ylable, fontproperties=myfont)
    plt.legend()
    plt.show()


def encrypto_per_file(owner_id):
    # 新建一个doctor对象，一个owner对象
    times = []
    doctor = Doctor()
    owner = Owner(owner_id)
    test = RecryptoUtil()
    ciphertext, capsule, time_used_encrypt = test.encrypto(
        owner.message, doctor.keys.recrypt_public_key)
    kfrags, timeUsed_approve = test.approve(doctor.keys.get_recrpto_private_Key(
    ), doctor.keys.get_recrpto_signer(), owner.keys.recrypt_public_key)
    cfrags, timeUsed_reencrypto = test.re_encrypto(
        capsule, kfrags, doctor.keys.recrypt_public_key, owner.keys.recrypt_public_key, doctor.keys.reencrypto_verifying_key)
    result, timeUsed_decrypto = test.decrypt(
        cfrags, capsule, owner.message, ciphertext, owner.keys.get_recrpto_private_Key())
    times.append(time_used_encrypt)
    times.append(timeUsed_approve)
    times.append(timeUsed_reencrypto)
    times.append(timeUsed_decrypto)
    print(result)
    return times

def draw_parament_serialization(title,xlable,ylable,line_lable,y_lim):
    draw_map = {}
    draw_map['title'] = title
    draw_map['xlable'] = xlable
    draw_map['ylable'] = ylable
    draw_map['line_lable'] = line_lable
    draw_map['y_lim'] = y_lim
    return draw_map
