import ecdsa
from ecdsa import SigningKey, NIST384p, VerifyingKey
import hashlib
def generate_key():
    """
    产生公钥和私钥
    :return: 二者组合
    """
    sk = SigningKey.generate(curve=NIST384p)
    vk = sk.get_verifying_key()
    return vk, sk


def make_transaction(sk, message):
    """
    加密交易
    :param sk_string: 私钥，用于签名
    :param message: 消息
    :return: 签名
    """
    signature = sk.sign(str(message).encode("utf8"),hashfunc=hashlib.sha256)  # 统一编码格式
    return signature


def is_valid(vk_string, message, signature):
    """
    验证交易是否合法
    :param vk_string: 公钥的字符串
    :param message: 消息
    :param signature: 签名
    :return: <bool> True合法，False不合法
    """
    vk = VerifyingKey.from_string(vk_string, NIST384p)
    try:
        vk.verify(signature, str(message).encode("utf8"),hashfunc=hashlib.sha256)  # 统一编码格式
        return True
    except:
        return False

