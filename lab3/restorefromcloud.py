import  os
import  boto3

ROOT_TARGET_DIR  =  '.'  # Root directory where files will be restored to
ROOT_S3_DIR  =  '24188516-cloudstorage'
s3  =  boto3.client("s3")

def  download_file(s3_key, local_file_path):
	local_dir  =  os.path.dirname(local_file_path)
	# Ensure the local directory exists
	if  not  os.path.exists(local_dir):
		print(f"Create directory {local_dir}")
		os.makedirs(local_dir)

	# Download the file
	s3.download_file(ROOT_S3_DIR, s3_key, local_file_path)
	print(f"Downloading {s3_key} to {local_file_path}")

# Main program
# List all objects in the S3 bucket
objects  =  s3.list_objects_v2(Bucket=ROOT_S3_DIR)
print(f"objects: %s", objects)
if  'Contents'  in  objects:
	for  obj  in  objects['Contents']:
		s3_key  =  obj['Key']
		local_file_path  =  os.path.join(ROOT_TARGET_DIR, s3_key).replace("/", os.path.sep)
		# Download the file from S3 to the corresponding local path
		download_file(s3_key, local_file_path)
else:
	print("No objects found in the bucket.")
	pass
	
print("done")