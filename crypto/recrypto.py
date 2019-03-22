# 关于重加密的操作
import time,os,sys
from umbral import pre, keys, signing
sys.path.append('/home/yapie/github/re-encryption/')
from util import type_convert
class RecryptoUtil(object):
    def encrypto(self,clear_text,doctor_public_key):
        crypto_start_time = time.time()
        ciphertext, capsule = pre.encrypt(doctor_public_key, clear_text)
        crypto_end_time = time.time()
        timeUsed = crypto_end_time - crypto_start_time
        return ciphertext,capsule,timeUsed
        
    def approve(self,doctor_private_key,doctor_signer,patient_public_key):
        approve_start_time = time.time()
        kfrags = pre.generate_kfrags(
            delegating_privkey=doctor_private_key,
                             signer=doctor_signer,
                             receiving_pubkey=patient_public_key,
                             threshold=1,
                             N=1)
        approve_end_time = time.time()
        timeUsed = approve_end_time - approve_start_time
        return kfrags,timeUsed

    def re_encrypto(self,capsule,kfrags,doctor_public_key,patient_public_key,doctor_verify_key):
        capsule.set_correctness_keys(
            delegating=doctor_public_key,
            receiving=patient_public_key,
            verifying=doctor_verify_key)
        cfrags = list()           # Bob's cfrag collection
        for kfrag in kfrags[:1]:
            cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)##代理进行重加密
            cfrags.append(cfrag)    # Bob收集重加密后的东西－－cfrag
        return cfrags

    def decrypt(self,cfrags,capsule,clear_text,ciphertext,patient_private_key):
        for cfrag in cfrags:   #用收集到的东西解密
            capsule.attach_cfrag(cfrag)
        cleartext = pre.decrypt(ciphertext=ciphertext, capsule=capsule,decrypting_key=patient_private_key)
        print(cleartext)
        if(cleartext == clear_text):
            return True
        else:
            return False
