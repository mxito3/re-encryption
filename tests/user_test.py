import sys
sys.path.append('/home/yapie/github/re-encryption/')
from user.user import User
if __name__ == "__main__":
    user=User()
    print(user.signup()) 