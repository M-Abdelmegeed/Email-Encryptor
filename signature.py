from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def sign_message(private_key, message):
    key = RSA.import_key(private_key)
    h = SHA256.new(message.encode('utf-8'))
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verify_signature(public_key, message, signature):
    key = RSA.import_key(public_key)
    h = SHA256.new(message.encode('utf-8'))
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False