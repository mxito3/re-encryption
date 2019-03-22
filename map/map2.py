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

need_test_file = 10


def init():
    config.set_default_curve(SECP256K1)


def encryptoTime_dataSize():
    result = []
    for index in range(common_operate.need_test_file):
        perResult = encrypto_per_file(index)
        result.append(perResult)
    print(result)


def encrypto_per_file(owner_id):
    # 新建一个doctor对象，一个owner对象
    doctor = Doctor()
    owner = Owner(owner_id)
    recrypto_util = RecryptoUtil()
      
    ciphertext, capsule, time_used = recrypto_util.encrypto(owner.message)

    kfrags, timeUsed1 = recrypto_util.approve()
    cfrags = recrypto_util.re_encrypto(capsule,kfrags)
    result = recrypto_util.decrypt(cfrags, capsule, plaintext)
    return time_used


encryptoTime_dataSize()
