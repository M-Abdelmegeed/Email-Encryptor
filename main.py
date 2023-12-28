import os
from aes import encrypt_content, decrypt_content
from hash import calculate_hash
from signature import generate_key_pair, sign_message, verify_signature

def main(mail):
    # Generate Key Pair for Digital Signature
    private_key, public_key = generate_key_pair()

    with open(mail, 'r') as file:
        email_content = file.read()

    # 1. Symmetric Encryption
    encryption_key = os.urandom(16)
    encrypted_data = encrypt_content(encryption_key, email_content)
    print(type(encrypted_data))
    print("Encrypted Data:", encrypted_data)

    # 2. Hashing
    hashed_data = calculate_hash(email_content)
    print("Hashed Data:", hashed_data)

    # 3. Digital Signature for Sender Verification
    signature = sign_message(private_key, email_content)
    print("Digital Signature:", signature)
    
    # 4. Decryption
    decrypted_content = decrypt_content(encryption_key, encrypted_data)
    print("Decrypted Content:", decrypted_content)

    hash_verification = calculate_hash(decrypted_content)
    print("Hash Verification:", hashed_data == hash_verification)

    signature_verification = verify_signature(public_key, decrypted_content, signature)
    print("Signature Verification:", signature_verification)

    # Write encrypted content to file
    encrypted_file_path = f'Encryptions/{mail.split("/")[1].split(".")[0]}_encrypted.txt'
    with open(encrypted_file_path, 'wb') as file:
        file.write(encrypted_data)
    print(f"Encrypted Data written to: {encrypted_file_path}")

    # Write decrypted content to file
    decrypted_file_path = f'Decryptions/{mail.split("/")[1].split(".")[0]}_decrypted.txt'
    with open(decrypted_file_path, 'w') as file:
        file.write(decrypted_content)
    print(f"Decrypted Content written to: {decrypted_file_path}")

main('EmailSamples/email2.txt')
# print(os.urandom(16))