import sys
sys.path.append('/home/yapie/github/re-encryption/')
from crypto import ecdas
from config import common
need_test_file = 10
from matplotlib.font_manager import  *
from umbral import config
from umbral.curve import SECP256K1
def init():
  config.set_default_curve(SECP256K1)

def getDataSize():
  result=[]
  for index in range(need_test_file):
    perSize= common.getDataSize(index)
    result.append(perSize)
  return result
def get_font():
  myfont = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
  return myfont