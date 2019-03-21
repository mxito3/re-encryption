from umbral import pre, keys, signing



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