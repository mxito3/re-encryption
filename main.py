from umbral import pre, keys, signing

# 为Alice生成密钥对
alices_private_key = keys.UmbralPrivateKey.gen_key()
alices_public_key = alices_private_key.get_pubkey()

alices_signing_key = keys.UmbralPrivateKey.gen_key()
alices_verifying_key = alices_signing_key.get_pubkey()
alices_signer = signing.Signer(private_key=alices_signing_key)

# 为Bob生成密钥对
bobs_private_key = keys.UmbralPrivateKey.gen_key()
bobs_public_key = bobs_private_key.get_pubkey()



# 用alices的私钥加密明文
plaintext = b'Hello! my nama is Yapie!' #明文，，换成你的病例就行了
ciphertext, capsule = pre.encrypt(alices_public_key, plaintext)

# 尝试用alice的私钥是否能够解密.
cleartext = pre.decrypt(ciphertext=ciphertext,
                        capsule=capsule,
                        decrypting_key=alices_private_key)

# Alice 生成　"M of N"　的解密条件，意思是bob能收到20个代理中的十个以上的重加密就可以解密密文
# In this example, 10 out of 20.
kfrags = pre.generate_kfrags(delegating_privkey=alices_private_key,
                             signer=alices_signer,
                             receiving_pubkey=bobs_public_key,
                             threshold=1,
                             N=1)

#代理重加密．bob确认收到的cfrags数量，大于10Bob便可以解密密文
capsule.set_correctness_keys(delegating=alices_public_key,
                             receiving=bobs_public_key,
                             verifying=alices_verifying_key)

cfrags = list()           # Bob's cfrag collection
for kfrag in kfrags[:1]:
  # kfrag是密钥吗？
  cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)##代理进行重加密
  cfrags.append(cfrag)    # Bob收集重加密后的东西－－cfrag


# Bob解密密文
for cfrag in cfrags:   #用收集到的东西解密
  capsule.attach_cfrag(cfrag)

bob_cleartext = pre.decrypt(ciphertext=ciphertext,
                            capsule=capsule,
                            decrypting_key=bobs_private_key)


print("Bob解密出的密文是%s"%bob_cleartext)
assert bob_cleartext == plaintext