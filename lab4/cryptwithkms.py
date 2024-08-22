import boto3

s3 = boto3.client('s3')
kms = boto3.client('kms')

BUCKET_NAME = "24188516-cloudstorage"
KMS_KEY = "alias/24188516"

def encrypt_file(file_key):
    # Get the file from bucket and read content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = s3_object['Body'].read()

    # Encrypt the file content using KMS
    encrypt_res = kms.encrypt(
        KeyId=KMS_KEY,
        Plaintext=file_content
    )
    file_body = encrypt_res['CiphertextBlob']
    encrypt_file_key = f"{file_key}.encrypted"

    # Add the encrypted file to bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=encrypt_file_key, Body=file_body)
    print("File encrypted as: ", encrypt_file_key, "with content: \n", file_body, "\n")
    
	# After encrypted file is uploaded, try to decrypt it
    decrypt_file(encrypt_file_key)

def decrypt_file(file_key):
    # Get the encrypted file from bucket and read content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = s3_object['Body'].read()

    # Decrypt the file content using KMS
    decrypt_res = kms.decrypt(
        KeyId=KMS_KEY,
        CiphertextBlob=file_content
    )
    plain_text = decrypt_res['Plaintext']
    file_body = plain_text.decode('utf-8') #convert plain text bytes to a regular string
    decrypted_file_key = f"{file_key}.decrypted"

    # Upload the decrypted content back to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_file_key, Body=file_body)
    print("File encrypted as: ", decrypted_file_key, "with content: \n", file_body, "\n")

def process_files(BUCKET_NAME, KMS_KEY):
    # List all files in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            encrypt_file(key)

if __name__ == "__main__":
    process_files(BUCKET_NAME, KMS_KEY)