import boto3
import json

STUDENT_NUMBER = '24188516'

def create_kms_key():
    # import the policy
    with open('kmspolicy.json', 'r') as policy_file:
        policy = json.load(policy_file)

    kms = boto3.client('kms')
    key_response = kms.create_key(
        Policy = json.dumps(policy),
        KeyUsage='ENCRYPT_DECRYPT',
        Origin='AWS_KMS'
    )
    key_id = key_response['KeyMetadata']['KeyId']

    # Create the alias for the KMS key
    alias_name = f'alias/{STUDENT_NUMBER}'
    alias_response = kms.create_alias(
        AliasName=alias_name,
        TargetKeyId=key_id
    )
    print(f"Key and alias generated successfully!")

if __name__ == "__main__":
    create_kms_key()