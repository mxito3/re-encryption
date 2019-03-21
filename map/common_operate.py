import sys
sys.path.append('/home/yapie/github/re-encryption/')
from config import ecdas,common
need_test_file = 10
def getDataSize():
  result=[]
  for index in range(need_test_file):
    perSize= common.getDataSize(index)
    result.append(perSize)
  return result