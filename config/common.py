def checkHash(message,message_hash):
    if hash(message) == message_hash:
        return True
    else:
        return False