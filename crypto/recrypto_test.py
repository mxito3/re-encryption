import sys
sys.path.append('/home/yapie/github/re-encryption/')
from recrypto import RecryptoUtil
from umbral import pre, keys, signing
from utils import type_convert
from user.doctor import Doctor
from user.owner import Owner
if __name__ == "__main__":
    owner_id = 0
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
    print(result)
  