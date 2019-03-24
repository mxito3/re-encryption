# 关于重加密的操作
import time,os,sys
sys.path.append('/home/yapie/github/re-encryption/')
from utils import type_convert
from umbral import pre, keys, signing

class RecryptoUtil(object):
    def encrypto(self,clear_text,owner_public_key):
        crypto_start_time = time.time()
        ciphertext, capsule = pre.encrypt(owner_public_key, clear_text)
        print('{}   {}'.format(sys.getsizeof(ciphertext),sys.getsizeof(capsule)))
        crypto_end_time = time.time()
        timeUsed = type_convert.double_process(crypto_end_time - crypto_start_time)
        return ciphertext,capsule,timeUsed
        
    def approve(self,owner_private_key,owner_signer,asker_public_key):
        approve_start_time = time.time()
        kfrags = pre.generate_kfrags(
            delegating_privkey=owner_private_key,
                             signer=owner_signer,
                             receiving_pubkey=asker_public_key,
                             threshold=1,
                             N=1)
        approve_end_time = time.time()
        timeUsed = type_convert.double_process(approve_end_time - approve_start_time)
        return kfrags,timeUsed

    def re_encrypto(self,capsule,kfrags,owner_public_key,asker_public_key,owner_verify_key):
        start_time = time.time()
        capsule.set_correctness_keys(
            delegating=owner_public_key,
            receiving=asker_public_key,
            verifying=owner_verify_key)
        cfrags = list()           # Bob's cfrag collection
        for kfrag in kfrags[:1]:
            cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)##代理进行重加密
            cfrags.append(cfrag)    # Bob收集重加密后的东西－－cfrag
        end_time = time.time()
        time_used = type_convert.double_process(end_time-start_time)
        return cfrags,time_used

    def decrypt(self,cfrags,capsule,clear_text,ciphertext,asker_private_key):
        start_time = time.time()
        for cfrag in cfrags:   #用收集到的东西解密
            capsule.attach_cfrag(cfrag)
        cleartext = pre.decrypt(ciphertext=ciphertext, capsule=capsule,decrypting_key=asker_private_key)
        end_time = time.time()
        time_used = type_convert.double_process(end_time-start_time)
        if(cleartext == clear_text):
            return True,time_used
        else:
            return False,time_used

