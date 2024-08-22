
<div  style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">
<h2>Labs 1-5</h2>
<p>Student ID: 24188515</p>
<p>Student Name: Dayu Liu</p>
</div>

# Lab 1
## AWS Account and Log in
### [1] Log into an IAM user account created for you on AWS.
After receiving the email with original login cridentials, I logged-in and reseted my password accordingly.
![enter image description here](http://127.0.0.1/assets/lab1-1.png)

### [2] Search and open Identity Access Management
Clicked on the top-right panel to access `security cridentials`
![enter image description here](http://127.0.0.1/assets/lab1-2.png)

Under the `access key` tab, create new access key and secret. Store the key and secret into somewhere private and secure.
![enter image description here](http://127.0.0.1/assets/lab1-3.png)

## Set up recent Linux OSes

I am running a windows machine, I decided to go with `ubuntus on windows` because it offers an isolated environment and separated file directory, which sets ease with file management.
![enter image description here](http://127.0.0.1/assets/lab1-4.png)

## Install Linux packages
### [1] Install Python 3.10.x
Because my ubuntu version is already `22.04`, I will get the lastest python version which is `3.10.12`.
To update apt to latest version:
```
sudo apt update
sudo apt -y upgrade
```
![enter image description here](http://127.0.0.1/assets/lab1-5.png)
To check the latest version of python:
`python3 -V`
![enter image description here](http://127.0.0.1/assets/lab1-6.png)
To install pip3:
`sudo apt install -y python3-pip`
![enter image description here](http://127.0.0.1/assets/lab1-7.png)

### [2] Install awscli
To install AWS CLI and upgrade to latest version:
`pip3 install awscli --upgrade`
![enter image description here](http://127.0.0.1/assets/lab1-8.png)

### [3] Configure AWS
To configure and connect to Amazon EC2:
`aws configure`
![enter image description here](http://127.0.0.1/assets/lab1-9.png)

### [4] Install boto3
I find this step redundant as `botocore` is already inluded in AWS Cli package, but just for the spirit:
`pip3 install boto3`
![enter image description here](http://127.0.0.1/assets/lab1-10.png)

## Test the installed environment
### [1] Test the AWS environment
To confirm that we are connected to the `AWS environment`, run a simple command which prints out the region table.
`aws ec2 describe-regions --output table`
![enter image description here](http://127.0.0.1/assets/lab1-11.png)

### [2] Test the Python environment
We executed a command offered by AWS-Cli in the terminal, now we want to test on the python environment to achive a similar goal:
```
python3
>>> import boto3
>>> ec2 = boto3.client('ec2')
>>> response = ec2.describe_regions()
>>> print(response)
```
![enter image description here](http://127.0.0.1/assets/lab1-12.png)

### [3] Write a Python script
Now we create a python script to wrap these lines in one file and also format the reponse into table structure.
The python script is located in `~\cits5503\lab1` in my Ubuntu machine.

#### (1) Install dependencies
The pandas library is used here to convert un-tabulated data into structured table.
Run the following code to install the extra dependency
`pip install pandas`

#### (2) Explain the code
The code in the script adds an extra step, the reponse data is sent as a parameter into pandas dataframe and then gets printed.
```
import boto3 as bt
import pandas as pd

ec2 = bt.client('ec2')
response = ec2.describe_regions()
regions = response['Regions']
regions_df = pd.DataFrame(regions)
print(regions_df)
```

#### (3) Run the script

run the following code to execute the python script:
`python3 lab1.py`

#### [4] Get the results
After the script is executed, results are printed in a table structure:
| --- | Endpoint | RegionName | OptInStatus |
| --- | --- | --- | --- |
0| ec2.ap-south-1.amazonaws.com| ap-south-1| opt-in-not-required
1| ec2.eu-north-1.amazonaws.com| eu-north-1| opt-in-not-required
2| ec2.eu-west-3.amazonaws.com| eu-west-3| opt-in-not-required
3| ec2.eu-west-2.amazonaws.com| eu-west-2| opt-in-not-required
4| ec2.eu-west-1.amazonaws.com| eu-west-1| opt-in-not-required
5| ec2.ap-northeast-3.amazonaws.com| ap-northeast-3| opt-in-not-required
6| ec2.ap-northeast-2.amazonaws.com| ap-northeast-2| opt-in-not-required
7| ec2.ap-northeast-1.amazonaws.com| ap-northeast-1| opt-in-not-required
8| ec2.ca-central-1.amazonaws.com| ca-central-1| opt-in-not-required
9| ec2.sa-east-1.amazonaws.com| sa-east-1| opt-in-not-required
10| ec2.ap-southeast-1.amazonaws.com| ap-southeast-1| opt-in-not-required
11| ec2.ap-southeast-2.amazonaws.com| ap-southeast-2| opt-in-not-required
12| ec2.eu-central-1.amazonaws.com| eu-central-1| opt-in-not-required
13| ec2.us-east-1.amazonaws.com| us-east-1| opt-in-not-required
14| ec2.us-east-2.amazonaws.com| us-east-2| opt-in-not-required
15| ec2.us-west-1.amazonaws.com| us-west-1| opt-in-not-required
16| ec2.us-west-2.amazonaws.com| us-west-2| opt-in-not-required

<div  style="page-break-after: always;"></div>

# Lab 2

## Create an EC2 instance using awscli
### [1] Create a security group
Create a security group with the name of my student number `24188516-sg`, `--group-name` specifies the group name and `--description` adds a description.
```
aws ec2 create-security-group --group-name 24188516-sg --description "security group for development environment"
```
![enter image description here](http://127.0.0.1/assets/lab2-1.png)
The response will return the GroupId being created.
### [2] Authorise inbound traffic for ssh
Create a rule to add tcp permission to this security group, `--protocol` specifies which internet protocol, `--port` specifies which port used for connection and `--cidr` specifies IP routing.
```
aws ec2 authorize-security-group-ingress --group-name 24188516-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
```
![enter image description here](http://127.0.0.1/assets/lab2-2.png)

The response will return the newly created rule along with specific rulesets.

### [3] Create a key pair
Now we need to create a `private key` and `public key` pair for encrypted connection. The `generated private key` is then saved as plain-text into `24188516-key.pem` file.
```
aws ec2 create-key-pair --key-name 24188516-key --query 'KeyMaterial' --output text > 24188516-key.pem
```

To use this key on Linux, copy the file to a directory ~/.ssh and change the permissions to:
```
chmod 400 24188516-key.pem
```
This grants the owner of the file read permission, the output is as follow:
![enter image description here](http://127.0.0.1/assets/lab2-3.png)
![enter image description here](http://127.0.0.1/assets/lab2-4.png)

### [4] Create the instance 
Because my student number is `24188516`, create an ec2 instance in `eu-north-1` region. `--image-id` specifies ami id with preset configurations, mine is `ami-07a0715df72e58928`. `--instance-type` is set to t2.micro, and we are using the private key `24188516-key`
```
 aws ec2 run-instances --image-id ami-07a0715df72e58928 --security-group-ids 24188516-sg --count 1 --instance-type t3.micro --key-name 24188516-key --query 'Instances[0].InstanceId'
 ```

For some reason, at the moment I was working on the lab, t2.micro container is not supported so I switched to t3.micro. The instance is created with instance id `i-0553e2ea0492e1c73`
![enter image description here](http://127.0.0.1/assets/lab2-6.png)
![enter image description here](http://127.0.0.1/assets/lab2-5.png)

### [5] Add a tag to your Instance
Now we have the instance id `i-0553e2ea0492e1c73`, add a tag that specifies the name, the value should be my student number with -vm `24188516-vm` for using single instance.
 ```
  aws ec2 create-tags --resources i-0553e2ea0492e1c73 --tags Key=Name,Value=24188516-vm
 ```

### [6] Get the public IP address
**describe-instances** returns available information to the instance with `--instance-ids`, since we only want the IP address for ssh purpose, the query limits the output to only `Reservations[0].Instances[0].PublicIpAddress`
```
aws ec2 describe-instances --instance-ids i-0553e2ea0492e1c73 --query 'Reservations[0].Instances[0].PublicIpAddress'
```
![enter image description here](http://127.0.0.1/assets/lab2-7.png)

### [7] Connect to the instance via ssh
Use the stored pem key to connect to the public IP `16.171.151.20` of the instance via SSH
```
ssh -i 24188516-key.pem ubuntu@16.171.151.20
```
Now that the server is connected, we can see system information on the console:
![enter image description here](http://127.0.0.1/assets/lab2-8.png)

### [8] List the created instance using the AWS console
The original instance from step 1-7 was destoyed over night so you might see the instance id has changed because I had to create a new one. This is the screenshot:
![enter image description here](http://127.0.0.1/assets/lab2-9.png)

## Create an EC2 instance with Python Boto3

The script uses **boto3** package instead of cli commands. Names of some of the methods and parameters can vary but they achieved the same goal. The **Group name, Key name and Instance name** all have an appendix **'-2'** to differentiate from the previous practice.

The code is as follows:
```
import  boto3  as  bt
import  os

# constants
GroupName  =  '24188516-sg-2'
KeyName  =  '24188516-key-2'
InstanceName=  '24188516-vm-2'

ec2  =  bt.client('ec2')

# 1 create security group
step1_response  =  ec2.create_security_group(
	Description="security group for development environment",
	GroupName=GroupName
)

# 2 authorise ssh inbound rule
step2_response  =  ec2.authorize_security_group_ingress(
	GroupName=GroupName,
	IpPermissions=[
		{
			'IpProtocol': 'tcp',
			'FromPort': 22,
			'ToPort': 22,
			'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
		}
	]
)

# 3 create key-pair
step3_response  =  ec2.create_key_pair(KeyName=KeyName)
PrivateKey  =  step3_response['KeyMaterial']
## save key-pair
with  open(f'{KeyName}.pem', 'w') as  file:
file.write(PrivateKey)
## grant file permission
os.chmod(f'{KeyName}.pem', 0o400)

# 4 create instance
step4_response  =  ec2.run_instances(
	ImageId='ami-07a0715df72e58928',
	SecurityGroupIds=[GroupName],
	MinCount=1,
	MaxCount=1,
	InstanceType='t3.micro',
	KeyName=KeyName
)
InstanceId  =  step4_response['Instances'][0]['InstanceId']

# 5 create tag
step5_repsonse  =  ec2.create_tags(
	Resources=[InstanceId],
	Tags=[
		{
		'Key': 'Name',
		'Value': InstanceName
		}
	]
)

# 6 get IP address
step6_response  =  ec2.describe_instances(InstanceIds=[InstanceId])
# Extract the public IP address
public_ip_address  =  step6_response['Reservations'][0]['Instances'][0]['PublicIpAddress']

# print all responses
print(f"{step1_response}\n{step2_response}\n{PrivateKey}\n{InstanceId}\n{step5_repsonse}\n{public_ip_address}\n")
```

After the script is executed, the repsonses of each step is printed as follows:
![enter image description here](http://127.0.0.1/assets/lab2-10.png)

Go to the AWS console to check the created instance;
![enter image description here](http://127.0.0.1/assets/lab2-11.png)

## Use Docker inside a Linux OS

### [1][2][3] Install and run Docker
This command is used to install necessary packages for the Docker service.
```
sudo apt install docker.io -y
```
This command is used to start the Docker service immediately.
```
sudo systemctl start docker
```
This command is used to enable the Docker service to start automatically at boot time.
```
sudo systemctl enable docker
```
![enter image description here](http://127.0.0.1/assets/lab2-12.png)

### [4] Check the version
After the Docker service is installed and enabled, run this command to check version and make sure it's working properly
```
docker --version
```
![enter image description here](http://127.0.0.1/assets/lab2-13.png)


### [5] Build and run an httpd container
The file index.html is located inside the html directory and add the following content, which does a single thing to display a paragraph with text **"Hello, World!"**.
```
  <html>
    <head> </head>
    <body>
      <p>Hello World!</p>
    </body>
  </html>
```

Create a file called Dockerfile outside the html directory with the following content. This specifies Docker to use Apache HTTP Server version 2.4 and copy whatever inside **/html** folder to the destination directory inside the Docker container, which is **/usr/local/apache2/htdocs/**
```
FROM httpd:2.4
COPY ./html/ /usr/local/apache2/htdocs/
```

Add my current user **liudayubob** to the docker group to grant permission, reboot uBuntus console and build the docker image 
```
sudo usermod -a -G docker <username>
```


Build a docker image. This command tells docker to build the image under the current **/html** directory and add a tag called **my-apache2**
```
docker build -t my-apache2 .
```
![enter image description here](http://127.0.0.1/assets/lab2-14.png)
Run the image. First parameter maps ports between the host machine and the Docker container to **port 80**, second paramater **'-dit'** runs the container in detached mode, keeps STDIN open and allocates a pseudo-TTY to let docker image run in background and enables interaction with the container. The container is named as **my-app** and uses **my-apache2** image built earlier.
```
docker run -p 80:80 -dit --name my-app my-apache2
```
![enter image description here](http://127.0.0.1/assets/lab2-15.png)

Open a browser and access address: http://localhost or http://127.0.0.1. The html page is hosted and prints out "Hello World!"
![enter image description here](http://127.0.0.1/assets/lab2-16.png)

### [6] Other docker commands

To check what is running.
```
docker ps -a
```
![enter image description here](http://127.0.0.1/assets/lab2-17.png)

This prints out some properties of the running container such as **Container ID, STATUS, PORTS**, with the corresponding container name and image name that we assigned.

To stop and remove the container
```
docker stop my-app
docker rm my-app
```

<div  style="page-break-after: always;"></div>

# Lab 3
### [1] Preparation
Files and directories are created as required, this is the following file structure with three files `cloudstorage.py`, `rootfile.txt` and `subfile.txt`
![enter image description here](http://127.0.0.1/assets/lab2-18.png)

### [2] Save to S3 by updating `cloudstorage.py`
The modified  `cloudstorage.py` is as followed, it will create an S3 bucket named `24188516-cloudstorage` if not existed, then traverse through all the directories and subdirectories in the root directory, and submit any discovered files to the `24188516-cloudstorage` bucket.

```
import os
import boto3
import base64

ROOT_DIR =  '.'
ROOT_S3_DIR =  '24188516-cloudstorage'
s3 = boto3.client("s3")

bucket_config = {'LocationConstraint': 'eu-north-1'}
def upload_file(folder_name, file, file_name):
	file_key = os.path.join(folder_name, file_name).replace("\\", "/")
	s3.upload_file(file, ROOT_S3_DIR, file_name) # file path, bucket name, key
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
```

The `s3.upload_file` methods takes in three parameters: **File path, Bucket name, File key**. We will concat both the *folder_name* and *file_name* as the file key, this way the file will be uploaded to the same file structure as our local machine.

![enter image description here](http://localhost/assets/lab2-19.png)

### [3] Restore from S3
Create a new program called `restorefromcloud.py` that reads the S3 bucket and writes the contents of the bucket within the appropriate directories.
`s3.list_objects_v2` will print all the files in the bucket along with their attributes such as **Key, Name**, etc. Join the local **ROOT_TARGET_DIR** with **Key** to form the local **local_file_path **. Check if local directory exists with `os.path.exists()`, if not create is with `os.makedirs()`, after that we can call `s3.download_file(ROOT_S3_DIR, s3_key, local_file_path)` with 3 parameters **Bucket, Key, Filename** to download the remote copy to corresponding local directory.
```
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
```
![enter image description here](http://localhost/assets/lab2-20.png)

### [4] Write information about files to DynamoDB

 1. Install DynamoDB

Create and jump into the dynamodb directory. Then install **JRE** and **DynamoDB** package and extract the tarball files on our lab3 folder. Once the DynamoDB package is extracted, there will be a java compiled code `DynamoDBLocal.jar` and a folder with libraries `DynamoDBLocal_lib`, which we use to run the DynamoDB instance.
```
mkdir dynamodb
cd dynamodb

# install jre
sudo apt-get install default-jre
# install dynamodb
wget https://s3-ap-northeast-1.amazonaws.com/dynamodb-local-tokyo/dynamodb_local_latest.tar.gz

# unzip dynamodb
tar -zxvf dynamodb_local_latest.tar.gz
```
![enter image description here](http://localhost/assets/lab2-21.png)

Start DynamoDBLocal instance on JRE environment, I will specify the `-port` number to **8001** since 8000 was already taken for other tasks on my machine. The `-sharedDb` parameter instructs to create a single database file named _shared-local-instance.db_. Every program that connects to DynamoDB accesses this file
```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar –sharedDb -port 8001
```
![enter image description here](http://localhost/assets/lab2-22.png)

2. Create table in DynamoDB
Create a `databaseoperation.py` script to create the table on DynamoDB, with the following attributes, where `userId` is the partition key and `fileName` is the sort key. `KeyType` indicates `HASH` for Partition key and `RANGE` for sort key. `AttributeName ` and `AttributeType` specify the name and the type of each attribute in the table.
 
 **Because DynamoDB is a schema-free database, attributes can be added directly when inserting items into the table, we don't need to declare 'path', 'lastUpdated', 'owner', 'permissions' to comply with AWS's coding standards**
 
```
# database schema
CloudFiles = {
	'userId',
	'fileName',
	'path',
	'lastUpdated',
	'owner',
	'permissions'
}
```
```
# createtable.py
import  boto3

def  create_db_table():
# initialize dynamodb service instance
dynamodb  =  boto3.resource('dynamodb', endpoint_url="http://localhost:8001")
table  =  dynamodb.create_table(
	TableName='CloudFiles',
	KeySchema=[
		{
		'AttributeName': 'userId',
		'KeyType': 'HASH'  # Partition key
		},
		{
		'AttributeName': 'fileName',
		'KeyType': 'RANGE'  # Sort key
		}
	],

	AttributeDefinitions=[
		{
		'AttributeName': 'userId',
		'AttributeType': 'S'
		},
		{
		'AttributeName': 'fileName',
		'AttributeType': 'S'
		}
	],
	ProvisionedThroughput={
		'ReadCapacityUnits': 1,
		'WriteCapacityUnits': 1
	}
)
print("Table status:", table.table_status)

if  __name__  ==  '__main__':
	create_db_table()
```
![enter image description here](http://localhost/assets/lab2-23.png)

3. Write data into the `CloudFiles` table
In this case, we will first use `s3.list_objects_v2()` to list all files in the `24188516-cloudstorage` bucket, the object in `s3.list_objects_v2()` contains **Key** and **LastModified**, to get extra attributes on **Owner, Permission**, we would do an extra call on `s3.get_object_acl` where these information can be found under **Grants** and **Owner** attributes. After we successfully extra all neccessary attributes, call `dynamodb_table.put_item()` to insert each object into the database. Because my region is in `eu-north-1`, we will fill owner Id into the owner field.

```
# writetable.py
import  boto3
import  os

BUCKET_NAME  =  '24188516-cloudstorage'
DB_NAME  =  'CloudFiles'

# Set up AWS instances for S3 and DynamoDB
s3  =  boto3.client('s3')
dynamodb  =  boto3.resource('dynamodb', endpoint_url="http://localhost:8001")
dynamodb_table  =  dynamodb.Table(DB_NAME)

def  list_files():
	# List all objects in the S3 bucket
	files  = []
	objects  =  s3.list_objects_v2(Bucket=BUCKET_NAME)
	if  'Contents'  in  objects:
	for  obj  in  objects['Contents']:
		# get access control list for owner and permission information
		obj_acl  =  s3.get_object_acl(Bucket=BUCKET_NAME, Key=obj['Key'])
		files.append({**obj, **obj_acl})
		return  files

def  extract_file_attributes(file):
	file_attributes  = {
		'userId': file['Grants'][0]['Grantee']['ID'],
		'fileName': os.path.basename(file['Key']),
		'path': file['Key'],
		'lastUpdated': file['LastModified'].isoformat(),
		'owner': file['Owner']['ID'],
		'permissions': file['Grants'][0]['Permission']
	}
	return  file_attributes

  

def  write_to_table():
# List all files in the bucket
try:
	files  =  list_files()
	# Iterate through each file
	for  file  in  files:
		# Extract attributes for a file
		file_attributes  =  extract_file_attributes(file)
		
		# Write the attributes to DynamoDB
		db_res  =  dynamodb_table.put_item(Item=file_attributes)
		print(f"Inserted {file_attributes['fileName']} into DynamoDB")
	
except  Exception  as  error:
	print("Database write operation failed: %s"  %  error)
	pass

if  __name__  ==  '__main__':
write_to_table()
```
![enter image description here](http://localhost/assets/lab2-24.png)


4. Print and destroy the `CloudFiles` table
Use AWS CLI command to scan the created DynamoDB table, the table structure can be shown below.
`aws dynamodb scan --table-name CloudFiles --endpoint-url http://localhost:8001`

![enter image description here](http://localhost/assets/lab2-25.png)


Use AWS CLI command to delete the created DynamoDB table. In this case, only the defined schema which are **Hash** and **Range** key will be printed.
`aws dynamodb delete-table --table-name CloudFiles --endpoint-url http://localhost:8001`

![enter image description here](http://localhost/assets/lab2-26.png)

<div  style="page-break-after: always;"></div>

# Lab 4
## Apply a policy to restrict permissions on bucket

### [1] Write a Python script
Apply the access permission policy to the S3 bucket `24188516-cloudstorage` in the last lab to allow only your username to access the bucket. The following code means to create a statement with user defined **Sid**, that **DENY** actions which are all **s3.*** actions to access resources in ``arn:aws:s3:::24188516-cloudstorage/*``, meaning all files under `24188516-cloudstorage` bucket, if the requesting user **aws:username** is not `24188516@student.uwa.edu.au`

The bucket policy as a JSON document, **Version** is the policy language recognized by AWS so we should keep it as `"2012-10-17"`, the **Statement** wraps our policy inside.
```
# bucketpolicy.json
{
	"Version": "2012-10-17",
	"Statement": {
		"Sid": "AllowAllS3ActionsInUserFolderForUserOnly",
		"Effect": "DENY",
		"Principal": "*",
		"Action": "s3:*",
		"Resource": "arn:aws:s3:::24188516-cloudstorage/*",
		"Condition": {
			"StringNotLike": {
				"aws:username":"24188516@student.uwa.edu.au"
			}
		}
	}
}
```

Because policy parameter only takes in JSON string, our policy is in JSON format. Open the `bucketpolicy.json`, load the json file with `json.load()` and then convert it into string with `json.dumps()`, finally call `s3.put_bucket_policy()` to apply the policy to our bucket.

```
# addpolicy.py
import boto3
import json

BUCKET_NAME =  '24188516-cloudstorage'

# Create an S3 instance
s3 = boto3.client('s3')

def  apply_bucket_policy():
	# Import the policy
	with  open('bucketpolicy.json', 'r') as policy_file:
		policy = json.load(policy_file)
		
	# stringify the policy to JSON document
	policy_string = json.dumps(policy)

	# Apply the policy to the bucket
	response = s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=policy_string)
	print("Policy applied!", response)

if  __name__  ==  '__main__':
	apply_bucket_policy()
```
![enter image description here](http://localhost/assets/lab4-1.png)

### [2] Check whether the script works
Test if the policy is applied with `aws s3api get-bucket-policy` on bucket `24188516-cloudstorage` and format the output the plain text
`aws s3api get-bucket-policy --bucket 24188516-cloudstorage --query Policy --output text`

![enter image description here](http://localhost/assets/lab4-2.png)

Now go to AWS console and see the result visually
![enter image description here](http://localhost/assets/lab4-3.png)

To check if the script works, assume I mess up the **username** and limit the access to only `12345678@student.uwa.edu.au`, now let's try to access the resources in the current user ~~`24188516@student.uwa.edu.au`~~. As expected, the access is **denied**.
![enter image description here](http://localhost/assets/lab4-4.png)

![enter image description here](http://localhost/assets/lab4-5.png)

## AES Encryption using KMS

### [1] Policy to be attached to KMS key
The following file `kmspolicy.json` contains the policy to be attached to the KMS key, which grants specific permissions to  root account and also IAM user which is me at 24188516@student.uwa.edu.au. First it grants the root user full access to all KMS operations `kms:*` on all resources `Resource: "*"`. Then it allows the IAM user to perform key management operations such as **creating, describing, enabling, disabling, tagging, and deleting** keys. Thirdly, it allows the IAM user to use the key for cryptographic operations like **encrypting, decrypting, re-encrypting, and generating data keys**. Lastly it allows the IAM user to manage grants (**create, list, revoke**) for the key only when the grant is for an AWS resource `kms:GrantIsForAWSResource`.

```
# kmspolicy.json
{
	"Version": "2012-10-17",
	"Id": "key-consolepolicy-3",
	"Statement": [
		{
			"Sid": "Enable IAM User Permissions",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::489389878001:root"
			},
			"Action": "kms:*",
			"Resource": "*"
		},
		{
			"Sid": "Allow access for Key Administrators",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::489389878001:user/24188516@student.uwa.edu.au"
			},
			"Action": [
				"kms:Create*",
				"kms:Describe*",
				"kms:Enable*",
				"kms:List*",
				"kms:Put*",
				"kms:Update*",
				"kms:Revoke*",
				"kms:Disable*",
				"kms:Get*",
				"kms:Delete*",
				"kms:TagResource",
				"kms:UntagResource",
				"kms:ScheduleKeyDeletion",
				"kms:CancelKeyDeletion"
			],
			"Resource": "*"
		},
		{
			"Sid": "Allow use of the key",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::489389878001:user/24188516@student.uwa.edu.au"
			},
			"Action": [
				"kms:Encrypt",
				"kms:Decrypt",
				"kms:ReEncrypt*",
				"kms:GenerateDataKey*",
				"kms:DescribeKey"
			],
			"Resource": "*"
		},
		{
			"Sid": "Allow attachment of persistent resources",
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::489389878001:user/24188516@student.uwa.edu.au"
			},
			"Action": [
				"kms:CreateGrant",
				"kms:ListGrants",
				"kms:RevokeGrant"
			],
			"Resource": "*",
			"Condition": {
				"Bool": {
					"kms:GrantIsForAWSResource": "true"
				}
			}
		}
	]
}
```

### [2] Attach a policy to the created KMS key
The following code will create a symmetric encryption KMS key with KMS key material, applying the above policy from the `kmspolicy.json` JSON file, specifying that the key is for encryption and decryption and use. Then it assigns an alias based on the student's ID, the generated alias follows the pattern that starts with `alias/*` resulting `alias/24188516`. 

```
import  boto3
import  json

STUDENT_NUMBER =  '24188516'

def  create_kms_key():
	# import the policy
	with  open('kmspolicy.json', 'r') as  policy_file:
		policy  =  json.load(policy_file)

	# Create a new KMS key with kmspolicy.json
	kms  =  boto3.client('kms')
	key_response  =  kms.create_key(
		Policy  =  json.dumps(policy),
		KeyUsage='ENCRYPT_DECRYPT',
		Origin='AWS_KMS'
	)
	key_id  =  key_response['KeyMetadata']['KeyId']

	# Create an alias for the KMS key
	alias_name  =  f'alias/{STUDENT_NUMBER}'
	alias_response  =  kms.create_alias(
		AliasName=alias_name,
		TargetKeyId=key_id
	)
	print(f"Key and alias generated successfully!")

	if  __name__  ==  "__main__":
		create_kms_key()
```
![enter image description here](http://localhost/assets/lab4-6.png)

### [3] Check whether the script works
Go to the KMS service in AWS console, as you can see the key is created with the alias of `24188516`, in the policy section,  	we can see that user 24188516@student.uwa.edu.au has been granted as the **Key Administrator** and **Key User**.
![enter image description here](http://localhost/assets/lab4-7.png)
![enter image description here](http://localhost/assets/lab4-8.png)

### [4] Use the created KMS key for encryption/decryption
- The following code in `cryptwithkms.py` first lists all the files in the specified S3 bucket `24188516-cloudstorage` and then Iterates over the list of files and calls **encrypt_file()** for each file with certain key.
- Inside **encrypt_file()** function, it retrieves the file content from `s3.get_object()`, encrypts the file content using the specified KMS key with `kms.encrypt()`. The result is returned in **CiphertextBlob** and we upload the encrypted content back to the bucket with a new key that appends _.encrypted_ to the original file name. After uploading the encrypted file, it calls the `decrypt_file()` function to decrypt the encrypted entity.
- Inside **decrypt_file()** function, it retrieves the file content in the same way, then we decrypt encrypted file content with `kms.decrypt()`. The result is the original **Plaintext Bytestring**. We shall convert the bytestring result into a regular string with `.decode('utf-8')`, then the decrypted content is uploaded back to the bucket with a new key that appends _.decrypted_ to the encrypted file name.

```
# cryptwithkms.py
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
```
![enter image description here](http://localhost/assets/lab4-9.png)

Now we can verify the result in AWS S3 console.
![enter image description here](http://localhost/assets/lab4-10.png)![enter image description here](http://localhost/assets/lab4-11.png)

### [5] Apply `pycryptodome` for encryption/decryption
Because AWS KMS also uses [AES with 256 bits-long](https://docs.aws.amazon.com/crypto/latest/userguide/awscryp-service-kms.html#awscryp-service-kms-using-and-managing), let's do the same with `pycryptodome`.

 1. First install the package
 Run `pip install pycryptodome`
 ![enter image description here](http://localhost/assets/lab4-12.png)
 
 2. Modify the above code in `cryptwithpycryptodome.py`
Now the code is very similar to `cryptwithkms.py`, with few exceptions:
- Import AES package for encryption/decryption and get_random_bytes for random key generation. The **AES_KEY** shall be **32 bytes** or 256 bits-long for consistency with **AWS KMS** approach.
```
	from Crypto.Cipher import AES
	from Crypto.Random import get_random_bytes
	
	AES_KEY  = get_random_bytes(32) # 32 bytes = 256 bits-long key
```

- For the encryption part, `AES.new(AES_KEY, AES.MODE_EAX)` initializes a new AES cipher object in EAX mode using the generated `AES_KEY`. `cipher.encrypt_and_digest()` converts the plaintext **file_content ** into **ciphertext** using AES algorithm and then generates an authentication **tag** to ensure the integrity of the data and get verified in decryption process.
- For the file_content,  it concatenates the **nonce, tag, and ciphertext** in this exact order into a single byte sequence (`file_body`). **nonce** is a unique value generatedto make sure the resulting ciphertext will be different
```
# Encrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(file_content) #  extract the ciphertext and tag from the encrypted content
    encrypt_file_key = f"{file_key}.encrypted"

    # Concatenate the nonce, tag, and the ciphertext
    file_body = cipher.nonce + tag + cipher_text
```


Write another Python script that uses the python library `pycryptodome` to encrypt and decrypt each file in the S3 bucket. Both encrypted and decrypted files will be in the same folder as the original file.

For encryption/decryption, refer to the example code from [fileencrypt.py](https://github.com/zhangzhics/CITS5503_Sem2/blob/master/Labs/src/fileencrypt.py)

**NOTE**: Delete the created S3 bucket and KMS key from AWS console after the lab is done.

## Answer the following question (Marked)

```
What is the performance difference between using KMS and using the custom solution?
```

<div  style="page-break-after: always;"></div>

# Lab 5
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExNjQ1NTY0MjEsLTYyNDM0Mzg3Nyw3Mz
UyMDY5MjksLTEwMjQyMDU0NCwtMTQyMjM0NzE4MCwzNzM4OTQz
NTAsLTIwNTAwMTIxMzIsLTk0ODE4NzQsNTYwODU5NDE2LDE0Mz
YzODQzNjYsLTkxMTY0MDYyMCwtMjA4ODc0NjYxMl19
-->
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTQ5OTU0NTkxOCwtMTI1MTM2MTQyNywtOT
I4MzkzOTcxLC0xOTU3MTI5NTYsNjk2OTcyMTU2LC0xNzg0MTY1
MTU4LC0xNzY2OTg5OTM2LC0xMDg3MDkyNjQwLC0yMDc0MjE3Nz
gsMTQxMzUwNDk1MywtMTEyODc1ODA0LC0yMDgwMjU3MDQyLDYw
MjMzOTc3OSwtNzM1MzI1OTE3LC0xNTMyOTUzMzMyLC05MTExMD
AyODMsLTE3NTAwODA5NjMsMjExNDgzNzk4OCwtNzYxMDU1MTE0
LDM4Mzk0NTAzMV19
-->