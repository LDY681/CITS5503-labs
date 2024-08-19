import boto3
import os

BUCKET_NAME = '24188516-cloudstorage'
DB_NAME = 'CloudFiles'

# Set up AWS instances for S3 and DynamoDB
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8001")
dynamodb_table = dynamodb.Table(DB_NAME)

def list_files():
    # List all objects in the S3 bucket
    files = []
    objects  =  s3.list_objects_v2(Bucket=BUCKET_NAME)
    if  'Contents'  in  objects:
        for  obj  in  objects['Contents']:
            # get access control list for owner and permission information
            obj_acl = s3.get_object_acl(Bucket=BUCKET_NAME, Key=obj['Key'])
            files.append({**obj, **obj_acl})    
    return files
          
def extract_file_attributes(file):
    file_attributes = {
        'userId': file['Grants'][0]['Grantee']['ID'],
        'fileName': os.path.basename(file['Key']),
        'path': file['Key'],
        'lastUpdated': file['LastModified'].isoformat(),
        'owner': file['Owner']['ID'],
        'permissions': file['Grants'][0]['Permission']
    }
    return file_attributes

def write_to_table():
    # List all files in the bucket
    try:
        files = list_files()
        # Iterate through each file
        for file in files:
            # Extract attributes for a file
            file_attributes = extract_file_attributes(file)
            # Write the attributes to DynamoDB
            db_res = dynamodb_table.put_item(Item=file_attributes)
            print(f"Inserted {file_attributes['fileName']} into DynamoDB")

    except Exception as error:
        print("Database write operation failed: %s" % error)
        pass

if __name__ == '__main__':
    write_to_table()
