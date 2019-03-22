import sys
sys.path.append('/home/yapie/github/re-encryption/')
from recrypto import RecryptoUtil
from umbral import pre, keys, signing
from util import type_convert
from config.doctor import Doctor
from config.owner import Owner
if __name__ == "__main__":
    owner_id = 0
    doctor = Doctor()
    owner = Owner(owner_id)
    test = RecryptoUtil()
    ciphertext,capsule,timeUsed=test.encrypto(owner.message,doctor.keys.recrypt_public_key)
    kfrags,timeUsed1=test.approve(doctor.keys.get_recrpto_private_Key(),doctor.keys.get_recrpto_signer(),owner.keys.recrypt_public_key)
    cfrags = test.re_encrypto(capsule,kfrags,doctor.keys.recrypt_public_key,owner.keys.recrypt_public_key,doctor.keys.reencrypto_verifying_key)
    result = test.decrypt(cfrags,capsule,owner.message,ciphertext, owner.keys.get_recrpto_private_Key())
    print(result)