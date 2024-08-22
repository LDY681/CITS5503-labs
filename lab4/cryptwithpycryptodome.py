import boto3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

s3 = boto3.client('s3')

BUCKET_NAME = "24188516-cloudstorage"
AES_KEY = get_random_bytes(32)  # 32 bytes = 256 bits-long key

def encrypt_file(file_key):
    # Get the file from the bucket and read content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = s3_object['Body'].read()

    # Encrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(file_content) # Extract the ciphertext and tag from the encrypted content
    encrypt_file_key = f"{file_key}.encrypted"

    # Concatenate the nonce, tag, and the ciphertext
    file_body = cipher.nonce + tag + cipher_text

    # Add the encrypted file to the bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=encrypt_file_key, Body=file_body)
    print(f"File encrypted as: {encrypt_file_key} with content: \n{file_body}\n")
    
    # After encrypted file is uploaded, try to decrypt it
    decrypt_file(encrypt_file_key)

def decrypt_file(file_key):
    # Get the encrypted file from the bucket and read content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_body = s3_object['Body'].read()

    # Parse the nonce, tag, and the ciphertext from the file content
    nonce = file_body[:16]  # 16 bytes for the nonce
    tag = file_body[16:32]  # 16 bytes for the tag
    cipher_text = file_body[32:] # The rest of the file content is the ciphertext

    # Decrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    plain_text = cipher.decrypt_and_verify(cipher_text, tag)
    file_body = plain_text.decode('utf-8') #convert plain text bytes to a regular string
    decrypted_file_key = f"{file_key}.decrypted"

    # Upload the decrypted content back to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_file_key, Body=file_body)
    print(f"File decrypted as: {decrypted_file_key} with content: \n{file_body}\n")

def process_files():
    print("Generated AES_KEY: ", AES_KEY, '\n')
    # List all files in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            encrypt_file(key)

if __name__ == "__main__":
    process_files()
