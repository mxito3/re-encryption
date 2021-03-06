from umbral import pre, keys, signing,params,config
from umbral.curve import SECP256K1
 # 为Alice生成密钥对
config.set_default_curve(SECP256K1)
alices_private_key = keys.UmbralPrivateKey.gen_key()
alices_public_key = alices_private_key.get_pubkey()

alices_signing_key = keys.UmbralPrivateKey.gen_key()
alices_verifying_key = alices_signing_key.get_pubkey()
alices_signer = signing.Signer(private_key=alices_signing_key)

 # 为Bob生成密钥对
bobs_private_key = keys.UmbralPrivateKey.gen_key()
bobs_public_key = bobs_private_key.get_pubkey()



 # 用alices的私钥加密明文
plaintext = b'Hello! my name is Yapie!' #明文，，换成你的病例就行了
ciphertext, capsule_temp = pre.encrypt(alices_public_key, plaintext)

capsule_bytes = capsule_temp.to_bytes()
parameters=params.UmbralParameters(SECP256K1)
capsule=pre.Capsule.from_bytes(capsule_bytes,parameters) 
 # 尝试用alice的私钥是否能够解密.
cleartext = pre.decrypt(ciphertext=ciphertext,
                        capsule=capsule,
                        decrypting_key=alices_private_key)

 # Alice 生成　"M of N"　的解密条件，意思是bob能收到20个代理中的十个以上的重加密就可以解密密文
# In this example, 10 out of 20.
kfrags = pre.generate_kfrags(delegating_privkey=alices_private_key,
                             signer=alices_signer,
                             receiving_pubkey=bobs_public_key,
                             threshold=10,
                             N=20)

 #代理重加密．bob确认收到的cfrags数量，大于10Bob便可以解密密文
capsule.set_correctness_keys(delegating=alices_public_key,
                             receiving=bobs_public_key,
                             verifying=alices_verifying_key)

cfrags = list()           # Bob's cfrag collection
for kfrag in kfrags[:10]:
  cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)
  cfrags.append(cfrag)    # Bob collects a cfrag


 # Bob解密密文
for cfrag in cfrags:
  capsule.attach_cfrag(cfrag)

bob_cleartext = pre.decrypt(ciphertext=ciphertext,
                            capsule=capsule,
                            decrypting_key=bobs_private_key)


print("Bob解密出的密文是%s"%bob_cleartext)
assert bob_cleartext == plaintext