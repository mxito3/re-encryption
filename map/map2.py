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
import threading
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
yminorLocator   = MultipleLocator(0.01)

def init():
    config.set_default_curve(SECP256K1)


def encryptoTime_dataSize():
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
    draw_map_all(encrypto, approve, re_encrypto, decrypto)


def draw_map_all(encrypto, approve, re_encrypto, decrypto):
    map1 = {}
    map1['title'] = u'医生授权时间与病例大小的关系'
    map1['xlable'] = u'病例大小(字节)'
    map1['ylable'] = u'病例授权时间'
    map1['line_lable'] = u'case approve time'

    map2 = {}
    map2['title'] = u'重加密时间与病例大小的关系'
    map2['xlable'] = u'病例大小(字节)'
    map2['ylable'] = u'重加密时间'
    map2['line_lable'] = u'case re_encrypto time'

    map3 = {}
    map3['title'] = u'解密时间与病例大小的关系'
    map3['xlable'] = u'病例大小(字节)'
    map3['ylable'] = u'解密时间'
    map3['line_lable'] = u'case decrypto time'

    map4 = {}
    map4['title'] = u'病例加密时间与病例大小的关系'
    map4['xlable'] = u'病例大小(字节)'
    map4['ylable'] = u'病例加密时间'
    map4['line_lable'] = u'case encrypto time'

    threading.Thread(target=draw_map, args=(
        map1['title'], map1['xlable'], map1['ylable'], map1['line_lable'], approve)).start()
    threading.Thread(target=draw_map, args=(
        map2['title'], map2['xlable'], map2['ylable'], map2['line_lable'], re_encrypto)).start()
    # threading.Thread(target=draw_map, args=(
        # map3['title'], map3['xlable'], map3['ylable'], map3['line_lable'], decrypto)).start()
    # threading.Thread(target=draw_map, args=(
        # map4['title'], map4['xlable'], map4['ylable'], map4['line_lable'], encrypto)).start()


def draw_map(title, xlable, ylable, line_lable, y):
    x, y = common.serializationDrawData(dataSize, y)
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


if __name__ == "__main__":
    dataSize = common_operate.getDataSize()
    encryptoTime_dataSize()
