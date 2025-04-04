import os
import boto3
import base64

ROOT_DIR =  '.'
ROOT_S3_DIR =  '24188516-cloudstorage'
s3 = boto3.client("s3")

bucket_config = {'LocationConstraint': 'eu-north-1'}
def upload_file(folder_name, file, file_name):
	file_key = os.path.join(folder_name, file_name).replace("\\", "/")
	s3.upload_file(file, ROOT_S3_DIR, file_key) # file path, bucket name, key
	print("Uploading %s"  %  file)

# Main program
# Insert code to create bucket if not there
try:
	response = s3.create_bucket(
		Bucket=ROOT_S3_DIR,
		CreateBucketConfiguration=bucket_config
	)
	print("Bucket created: $s"  % response)
except  Exception  as error:
	print("Bucket creation failed: %s"  % error)
	pass

# parse directory and upload files
for dir_name, subdir_list, file_list in os.walk(ROOT_DIR, topdown=True):
	if dir_name != ROOT_DIR:
		for fname in file_list:
			upload_file("%s/"  % dir_name[2:], "%s/%s"  % (dir_name, fname), fname)
print("done")