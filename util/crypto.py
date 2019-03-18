import hashlib
class Crypto(object):
    @staticmethod
    def generateId(acads_public_key):
        key_hash=hashlib.sha256()
        key_hash.update(str(acads_public_key).encode('utf-8'))
        hash_digest = key_hash.hexdigest()
        # print(hash_digest)
        result=hashlib.new('ripemd160')
        result.update(str(hash_digest).encode('utf-8'))
        return result.hexdigest()
    # def (self, parameter_list):
    #     pass

