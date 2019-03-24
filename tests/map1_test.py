import sys
sys.path.append('/home/yapie/github/re-encryption/')
from map import map1,common_operate
if __name__ == "__main__":
  common_operate.init()
  dataSize =common_operate.getDataSize()
  result= map1.verifyTime_dataSize()