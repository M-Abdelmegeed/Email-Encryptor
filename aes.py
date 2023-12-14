from Cryptodome.Cipher import AES
# from Cryptodome.Random import get_random_bytes
import os

def encrypt_content(key, content):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(content.encode('utf-8'))
    return cipher.nonce + tag + ciphertext

def decrypt_content(key, encrypted_data):
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_content = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_content.decode('utf-8')