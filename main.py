from umbral import pre, keys, signing,config
from config.doctor import Doctor
from umbral.curve import SECP256K1
from config import ecdas
from config.owner import Owner
from config import common
if __name__ == "__main__":
  config.set_default_curve(SECP256K1)

  #paint重加密密钥对
  paint_private_key = keys.UmbralPrivateKey.gen_key()
  paint_public_key = paint_private_key.get_pubkey()
  
  #doctor重加密密钥对
  doctor_private_key = keys.UmbralPrivateKey.gen_key()
  doctor_public_key = doctor_private_key.get_pubkey()
  doctor_public_key_string="".join(map(chr, doctor_public_key.to_bytes()))

  docter = Doctor()

  #为医生生成ecads
  doctor_verify_key, doctor_sign_key =ecdas.generate_key() 
  
  
  # 产生公钥和私钥
  doctor_verify_key_string = doctor_verify_key.to_string()

  #第一步
  ciphertext = docter.pretreatment(paint_public_key,doctor_public_key_string,doctor_sign_key)

  print(ciphertext)

  #第二步，owner确认信息是否正确
  owner=Owner()
  sign=ciphertext.get('sign')
  message = ciphertext.get('cipherHash')
  print(sign)
  print(message)
  verifyResult=owner.checkValid(doctor_verify_key_string,message,sign)
  if not verifyResult:
    print("医生签名验证失败")
    exit
  print("医生签名验证成功")


  #验证hash
  cipher_hash=message
  cipher_checker = ciphertext['cipher_checker']
  if not common.checkHash(cipher_checker,cipher_hash):
    print("c0或其hash值在传输的时候被破坏")
  else:
    print("c0 hash值验证成功")
  
  
  


  
  #病人解密

  # cleartext = pre.decrypt(ciphertext=ciphertext,
  #                       capsule=capsule,
  #                       decrypting_key=paint_private_key)
  
  # print(cleartext.decode("utf-8"))


  