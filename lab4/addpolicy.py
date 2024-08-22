import boto3
import json

BUCKET_NAME = '24188516-cloudstorage'

# Create an S3 instance
s3 = boto3.client('s3')

def apply_bucket_policy():
    # import the policy
    with open('bucketpolicy.json', 'r') as policy_file:
        policy = json.load(policy_file)

    # stringify the policy to JSON document
    policy_string = json.dumps(policy)
    
    print("policy_string: ", policy_string)
    # Apply the policy to the bucket
    response = s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=policy_string)
    print("Policy applied!", response)

if __name__ == '__main__':
    apply_bucket_policy()
