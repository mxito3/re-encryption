# 关于重加密的操作
import time,os,sys
from umbral import pre, keys, signing
sys.path.append('/home/yapie/github/re-encryption/')
from util import type_convert
class RecryptoUtil(object):
    def __init__(self,doctor_public_key, doctor_private_key,doctor_signer,doctor_verify_key,patient_public_key,patient_private_key):
        self.doctor_public_key =doctor_public_key
        self.doctor_private_key = doctor_private_key
        self.doctor_signer = doctor_signer
        self.doctor_verify_key = doctor_verify_key
        self.patient_public_key = patient_public_key
        self.patient_private_key = patient_private_key
    def encrypto(self,clear_text):
        crypto_start_time = time.time()
        ciphertext, capsule = pre.encrypt(self.doctor_public_key, clear_text)
        crypto_end_time = time.time()
        timeUsed = crypto_end_time - crypto_start_time
        return ciphertext,capsule,timeUsed
        
    def approve(self):
        approve_start_time = time.time()
        kfrags = pre.generate_kfrags(delegating_privkey=self.doctor_private_key,
                             signer=self.doctor_signer,
                             receiving_pubkey=self.patient_public_key,
                             threshold=1,
                             N=1)
        approve_end_time = time.time()
        timeUsed = approve_end_time - approve_start_time
        return kfrags,timeUsed

    def re_encrypto(self,capsule):
        capsule.set_correctness_keys(delegating=self.doctor_public_key,
                             receiving=self.patient_public_key,
                             verifying=self.doctor_verify_key)
        cfrags = list()           # Bob's cfrag collection
        for kfrag in kfrags[:1]:
            cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)##代理进行重加密
            cfrags.append(cfrag)    # Bob收集重加密后的东西－－cfrag
        return cfrags

    def decrypt(self,cfrags,capsule,data):
        for cfrag in cfrags:   #用收集到的东西解密
            capsule.attach_cfrag(cfrag)
        cleartext = pre.decrypt(ciphertext=ciphertext,
                        capsule=capsule,
                        decrypting_key=self.patient_private_key)
        print(cleartext)
        if(cleartext == data):
            return True
        else:
            return False

if __name__ == "__main__":
    plaintext = b'Hello! my name is Yapie!' 
    alices_private_key = keys.UmbralPrivateKey.gen_key()
    alices_public_key = alices_private_key.get_pubkey()
    alices_signing_key = keys.UmbralPrivateKey.gen_key()    
    alices_verifying_key = alices_signing_key.get_pubkey()
    alices_signer = signing.Signer(private_key=alices_signing_key)
    bobs_private_key = keys.UmbralPrivateKey.gen_key()
    bobs_public_key = bobs_private_key.get_pubkey()
    test = RecryptoUtil(alices_public_key,alices_private_key,alices_signer,alices_verifying_key,bobs_public_key,bobs_private_key)
    ciphertext,capsule,timeUsed=test.encrypto(plaintext)
    kfrags,timeUsed1=test.approve()
    cfrags = test.re_encrypto(capsule)
    result = test.decrypt(cfrags,capsule,plaintext)
    print(result)