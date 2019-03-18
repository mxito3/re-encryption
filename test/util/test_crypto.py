import sys
sys.path.append('/home/yapie/github/re-encryption/util')
from ...util import crypto


if __name__ == "__main__":
    id = Crypto.generateId()
    #test generateId
    print(id)
