from recrypto import RecryptoUtil
from umbral import pre, keys, signing
from util import type_convert
if __name__ == "__main__":
    plaintext = b'Hello! my name is Yapie!' 
    alice_private_key = keys.UmbralPrivateKey.gen_key()
    alice_public_key = alice_private_key.get_pubkey()
    alice_signing_key = keys.UmbralPrivateKey.gen_key()    
    alice_verify_key = alice_signing_key.get_pubkey()
    alice_signer = signing.Signer(private_key=alice_signing_key)
    bobs_private_key = keys.UmbralPrivateKey.gen_key()
    bobs_public_key = bobs_private_key.get_pubkey()
    
    test = RecryptoUtil()
    ciphertext,capsule,timeUsed=test.encrypto(plaintext,alice_public_key)
    kfrags,timeUsed1=test.approve(alice_private_key,alice_signer,bobs_public_key)
    cfrags = test.re_encrypto(capsule,kfrags,alice_public_key,bobs_public_key,alice_verify_key)
    result = test.decrypt(cfrags,capsule,plaintext,ciphertext, bobs_private_key)
    print(result)