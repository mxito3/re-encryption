import sys
sys.path.append('/home/yapie/github/re-encryption/')
from map import map2,common_operate
if __name__ == "__main__":
  common_operate.init()
  dataSize =common_operate.getDataSize()
  result= map2.encryptoTime_dataSize(dataSize)