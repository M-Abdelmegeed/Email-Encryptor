import win32com.client
import os
from aes import encrypt_content, decrypt_content
from hash import calculate_hash
from signature import generate_key_pair, sign_message, verify_signature

private_key, public_key = generate_key_pair()

def send_email(encryption_key,to, subject, body, attachment_paths=None):
    outlook_app = win32com.client.Dispatch("Outlook.Application")
    mail_item = outlook_app.CreateItem(0)
    mail_item.To = to
    mail_item.Subject = subject
    mail_item.Body = body
    
    signature = sign_message(private_key, body)
    signature_file_path = "C:/Users/DELL/Desktop/Semester 9/Computer and Networks Security/Encryption Algorithms/Signatures/DigitalSignature.txt"
    message_file_path = "C:/Users/DELL/Desktop/Semester 9/Computer and Networks Security/Encryption Algorithms/Messages/Message.txt"
    with open(signature_file_path, 'wb') as signature_file:
        signature_file.write(signature)
        
    mail_item.Attachments.Add(signature_file_path)
    
    encrypted_body = encrypt_content(encryption_key, body)
    print("Encrypted Body: ", encrypted_body)
    with open(message_file_path, 'wb') as message_file:
        message_file.write(encrypted_body)
    # mail_item.Attachments.Add(message_file_path)
    mail_item.Body = encrypted_body

    if attachment_paths:
        for attachment_path in attachment_paths:
            attachment = os.path.abspath(attachment_path)
            if os.path.exists(attachment):
                mail_item.Attachments.Add(attachment)
            else:
                print(f"Attachment file not found: {attachment_path}")

    mail_item.Send()


def read_emails(subject_to_find, encryption_key, save_attachment_path="C:/Users/DELL/Desktop/Semester 9/Computer and Networks Security/Encryption Algorithms/Attachments"):
    outlook_app = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook_app.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)  # 6 represents olFolderInbox constant
    items = inbox.Items

    body = None

    for item in items:
        print("Subject:", item.Subject)
        print("Sender:", item.SenderName)
        print("Received Time:", item.ReceivedTime)

        # Check if the subject matches the specified subject_to_find
        if item.Subject == subject_to_find:
            # Verify digital signature
            signature_attachment = None

            for attachment in item.Attachments:
                if attachment.FileName == "DigitalSignature.txt":
                    signature_attachment = attachment
                    break

            if signature_attachment is not None:
                # Save the signature attachment to a relative path
                signature_path = "C:/Users/DELL/Desktop/Semester 9/Computer and Networks Security/Encryption Algorithms/Signatures/DigitalSignature.txt"
                message_path = "C:/Users/DELL/Desktop/Semester 9/Computer and Networks Security/Encryption Algorithms/Messages/Message.txt"

                # Read the contents of the signature attachment directly
                with open(signature_path, 'rb') as signature_file:
                    signature = signature_file.read()
                print("Digital Signature Contents:", signature)
                with open(message_path, 'rb') as message_file:
                    message = message_file.read()
                encrypted_body = item.Body
                print("Encrypted Content:", encrypted_body)
                body = decrypt_content(encryption_key, message)
                print("Decrypted Content:", body)
                if verify_signature(public_key, body, signature):
                    print("Signature Verification: Successful")
                else:
                    print("Signature Verification: Failed")
            break

        print("\n")
    
    return body


if __name__ == "__main__":
    subject =  "Test Subject 28"
    receiver = "19p1298@eng.asu.edu.eg"
    sample_encryption_key = os.urandom(16)
    
    with open('EmailSamples/email4.txt', 'r') as file:
        email_content = file.read()
    send_email(sample_encryption_key, receiver, subject, email_content,
               ["EmailSamples/email4.txt"])
    hashed_data = calculate_hash(email_content)
    print('Sent Hashed Data: ', hashed_data)

    print("Waiting for email to be received...")
    input("Press Enter when the email is received.")
    
    print("Reading emails from Inbox and saving attachments:")
    decrypted_content = read_emails(subject_to_find=subject, encryption_key=sample_encryption_key)
    hash_verification = calculate_hash(decrypted_content)
    print("Hash Verification:", hashed_data == hash_verification)
