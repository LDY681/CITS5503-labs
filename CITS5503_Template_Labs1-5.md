
<div  style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">
<h2>Labs 1-5</h2>
<p>Student ID: 24188515</p>
<p>Student Name: Dayu Liu</p>
</div>

# Lab 1
## AWS Account and Log in
### [1] Reset and Login into IAM User Account
To start with, I received an email with the initial login credentials for my IAM user account. After navigating to the AWS login portal, I successfully logged in using these credentials and promptly reset my password as instructed.

![enter image description here](http://127.0.0.1/assets/lab1-1.png)

This step grants access to the AWS Management Console, which provides all necessary resources and services for managing AWS infrastructure.

### [2] Access Identity and Access Management (IAM)
After logging in, I saw a clickable with my `IAM user` and `Account ID` information on the top-right corner. Once opened, I clicked on the top-right user panel to access `Security Credentials`.

![enter image description here](http://127.0.0.1/assets/lab1-2.png)

Within the `Access keys` tab, I created a new access key and secret. These credentials can be used for programmatic access to AWS services, allowing you to interact with AWS through command-line interfaces (CLI), SDKs, or APIs. It's important to securely store these credentials in a private location, as they grant significant access to your AWS resources.

![enter image description here](http://127.0.0.1/assets/lab1-3.png)

## Set up recent Linux OSes
Since I am running a Windows machine, I chose to set up `Ubuntu on Windows` via the Windows Subsystem for Linux (WSL). This option provides an isolated Linux environment with a separate file directory, making file management easier and more organized within the Windows system.

![enter image description here](http://127.0.0.1/assets/lab1-4.png)

By using WSL, I can run Linux-based commands and utilities without the need for a virtual machine or dual-boot setup, which saves both time and resources. This approach is ideal for development work where access to Linux-based tools is necessary while maintaining the flexibility of a Windows system.


## Install Linux Packages

### 1. Install Python 3.10.x
Since my Ubuntu version is `22.04`, I automatically receive the latest stable Python version, which is `3.10.12`.

#### Update Packages
Before installing Python, let's ensure our system's packages are up to date. Run the following commands to update and upgrade packages:
```bash
sudo apt update
sudo apt -y upgrade
```
![Updating System](http://127.0.0.1/assets/lab1-5.png)

#### Verify Python Version
Once updated, verify the version of Python installed by using the command:
```bash
python3 -V
```
This should display the Python version as `3.10.12`.

![Check Python Version](http://127.0.0.1/assets/lab1-6.png)

#### Install pip3
To manage Python packages, install `pip3`, the most popular package installer for Python to install third-party libraries and dependencies. Use the following command:
```bash
sudo apt install -y python3-pip
```
This command installs `pip3` and confirms the installation.

![Installing pip3](http://127.0.0.1/assets/lab1-7.png)

### 2. Install AWS CLI
To interact with AWS services from the command line, the AWS CLI (Command Line Interface) tool is neccessary. Install and upgrade AWS CLI to the latest version using the following command:
```bash
pip3 install awscli --upgrade
```
This ensures that we have the most recent version of AWS CLI with latest features and updates, to interact with AWS resources such as EC2, S3, etc.

![Install AWS CLI](http://127.0.0.1/assets/lab1-8.png)

### 3. Configure AWS CLI
After installation, configure the AWS CLI to connect to our Amazon EC2 instance. This is done by entering your credentials (Access Key ID, Secret Access Key, Region) using the following command:
```bash
aws configure
```
These credentials can be found from step [3]. These configurations help us to set up our AWS environment correctly and accessing AWS services securely.

![Configure AWS CLI](http://127.0.0.1/assets/lab1-9.png)



### 4. Install boto3
Although `botocore` is included with the AWS CLI package, `boto3` the AWS SDK for Python is used to send API requests and automate tasks via Python scripts, such as launching EC2 instances or managing S3 buckets. Install `boto3` using the following command:
```bash
pip3 install boto3
```

![Install boto3](http://127.0.0.1/assets/lab1-10.png)


## Test the Installed Environment

### 1. Test the AWS Environment
To confirm that we are properly connected to the AWS environment, we run a simple command that prints out the region table. This helps us verify that our AWS CLI configuration is correct and functional:
```bash
aws ec2 describe-regions --output table
```

This command queries the available regions in our AWS account and displays the information in a structured table format.

![AWS Region Table](http://127.0.0.1/assets/lab1-11.png)

### 2. Test the Python Environment
After confirming the AWS CLI is working, we now test the Python environment using `boto3`, the AWS SDK for Python. Our goal is to achieve a similar output to the previous test, but this time within the Python environment:
```python
python3
>>> import boto3
>>> ec2 = boto3.client('ec2')
>>> response = ec2.describe_regions()
>>> print(response)
```

This code snippet runs directly from the Python command line,  connects to the EC2 service through `boto3` and retrieves the list of regions in JSON format, demonstrating that the Python environment is correctly set up.

![Python Region Response](http://127.0.0.1/assets/lab1-12.png)


### 3. Write a Python Script
Now we create a Python script to wrap these lines into a single file and format the response into a structured table. The Python script is located in `~\cits5503\lab1` on our Ubuntu machine.

#### (1) Install Dependencies
We use the `pandas` library to convert un-tabulated data into a structured table. To install this additional dependency, run the following command:
```bash
pip install pandas
```

#### (2) Code Explanation
The code in the script adds an extra step. After retrieving the region data from AWS, we pass the response into a `pandas` dataframe to format and print the output in a table structure.

```python
import boto3 as bt
import pandas as pd

ec2 = bt.client('ec2')
response = ec2.describe_regions()
regions = response['Regions']
regions_df = pd.DataFrame(regions)
print(regions_df)
```

- **`boto3 as bt`**: Import `boto3`, aliased as `bt`, to interact with AWS services.
- **`pandas as pd`**: Import `pandas`, aliased as `pd`, to structure our data into a table.
- **`ec2 = bt.client('ec2')`**: Connect to the EC2 service.
- **`response = ec2.describe_regions()`**: Retrieve the available AWS regions.
- **`pd.DataFrame(regions)`**: Convert the regions data into a pandas DataFrame for structured output.

#### (3) Run the Script
To execute the Python script, use the following command:
```bash
python3 lab1.py
```

#### 4. Get the Results
After running the script, the results are printed in a table format:

| --- | Endpoint | RegionName | OptInStatus |
| --- | --- | --- | --- |
| 0 | ec2.ap-south-1.amazonaws.com | ap-south-1 | opt-in-not-required |
| 1 | ec2.eu-north-1.amazonaws.com | eu-north-1 | opt-in-not-required |
| 2 | ec2.eu-west-3.amazonaws.com | eu-west-3 | opt-in-not-required |
| 3 | ec2.eu-west-2.amazonaws.com | eu-west-2 | opt-in-not-required |
| 4 | ec2.eu-west-1.amazonaws.com | eu-west-1 | opt-in-not-required |
| 5 | ec2.ap-northeast-3.amazonaws.com | ap-northeast-3 | opt-in-not-required |
| 6 | ec2.ap-northeast-2.amazonaws.com | ap-northeast-2 | opt-in-not-required |
| 7 | ec2.ap-northeast-1.amazonaws.com | ap-northeast-1 | opt-in-not-required |
| 8 | ec2.ca-central-1.amazonaws.com | ca-central-1 | opt-in-not-required |
| 9 | ec2.sa-east-1.amazonaws.com | sa-east-1 | opt-in-not-required |
| 10 | ec2.ap-southeast-1.amazonaws.com | ap-southeast-1 | opt-in-not-required |
| 11 | ec2.ap-southeast-2.amazonaws.com | ap-southeast-2 | opt-in-not-required |
| 12 | ec2.eu-central-1.amazonaws.com | eu-central-1 | opt-in-not-required |
| 13 | ec2.us-east-1.amazonaws.com | us-east-1 | opt-in-not-required |
| 14 | ec2.us-east-2.amazonaws.com | us-east-2 | opt-in-not-required |
| 15 | ec2.us-west-1.amazonaws.com | us-west-1 | opt-in-not-required |
| 16 | ec2.us-west-2.amazonaws.com | us-west-2 | opt-in-not-required |

<div  style="page-break-after: always;"></div>

# 
# Lab 2

## Create an EC2 Instance Using AWS CLI

### 1. Create a Security Group
We start by creating a security group with the name based on our student number, `24188516-sg`. The `--group-name` flag specifies the group name, and `--description` provides a description of the group.
```bash
aws ec2 create-security-group --group-name 24188516-sg --description "security group for development environment"
```

This command creates a new security group, and the response will return the `GroupId` for the created group.

![Create Security Group](http://127.0.0.1/assets/lab2-1.png)

### 2. Authorize Inbound Traffic for SSH
Next, we add a rule to allow SSH access via TCP. The `--protocol` flag specifies the internet protocol, `--port` indicates the port used for the connection, and `--cidr` defines the IP range allowed access (in this case, `0.0.0.0/0` allows access from any IP).
```bash
aws ec2 authorize-security-group-ingress --group-name 24188516-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
```

This command creates a rule allowing SSH traffic on port **22**, and the response will display the newly created rule along with specific rulesets.

![Authorize Inbound Traffic](http://127.0.0.1/assets/lab2-2.png)

### 3. Create a Key Pair
To establish a secure, encrypted connection to the EC2 instance, we generate a private and public key pair. The generated private key is saved as plain text in the `24188516-key.pem` file.
```bash
aws ec2 create-key-pair --key-name 24188516-key --query 'KeyMaterial' --output text > 24188516-key.pem
```

Once the key is created, we ensure it has the correct permissions by copying the file to the `~/.ssh` directory and granting permissions with `chmod`:
```bash
chmod 400 24188516-key.pem
```

This command grants the owner of the file **read-only** permissions to secure the key. Below is the output after successfully creating and securing the key:

![Key Pair Creation](http://127.0.0.1/assets/lab2-3.png)
![Permission Change](http://127.0.0.1/assets/lab2-4.png)

### 4. Create the Instance
Since my student number is `24188516`, create an EC2 instance in the `eu-north-1` region. The `--image-id` specifies the AMI ID with preset configurations; in this case, the AMI ID is `ami-07a0715df72e58928`. The instance type is set to `t3.micro`, and we use the private key `24188516-key` for secure access.

```bash
aws ec2 run-instances --image-id ami-07a0715df72e58928 --security-group-ids 24188516-sg --count 1 --instance-type t3.micro --key-name 24188516-key --query 'Instances[0].InstanceId'
```

At the time of running the lab, the **t2.micro** instance type was not supported, so we switched to **t3.micro**. The instance was successfully created with the instance ID `i-0553e2ea0492e1c73`.

![Create EC2 Instance](http://127.0.0.1/assets/lab2-6.png)
![Instance ID](http://127.0.0.1/assets/lab2-5.png)

### 5. Add a Tag to the Instance
Now that we have the instance ID `i-0553e2ea0492e1c73`, we add a tag to name the instance. The tag key is `Name`, and the value is our student number followed by `-vm`, so the tag is `24188516-vm`.

```bash
aws ec2 create-tags --resources i-0553e2ea0492e1c73 --tags Key=Name,Value=24188516-vm
```

### 6. Get the Public IP Address
To retrieve the public IP address of the instance, we use the `describe-instances` command. The query limits the output to only the `PublicIpAddress` of the instance:

```bash
aws ec2 describe-instances --instance-ids i-0553e2ea0492e1c73 --query 'Reservations[0].Instances[0].PublicIpAddress'
```

This IP address is needed for SSH access to the instance.

![Public IP Address](http://127.0.0.1/assets/lab2-7.png)

### 7. Connect to the Instance via SSH
Now, we connect to the instance using the public IP address `16.171.151.20` via SSH. We use the previously generated `.pem` file to authenticate:

```bash
ssh -i 24188516-key.pem ubuntu@16.171.151.20
```

After connecting, we can see system information on the console, indicating that the connection was successful.

![SSH Connection](http://127.0.0.1/assets/lab2-8.png)

### 8. List the Created Instance Using the AWS Console
The original instance created in steps 1-7 was destroyed overnight, so I had to run the commands again and the instance ID would differ. Here is a screenshot of the sucessfully created instance from the AWS console:

![AWS Console](http://127.0.0.1/assets/lab2-9.png)

## Create an EC2 Instance with Python Boto3

In this step, we create an EC2 instance using the **boto3** Python package instead of AWS CLI commands. Although some method names and parameters differ, the result is the same as in the previous steps. To differentiate from the previous instance, we append `'-2'` to the **Group name**, **Key name**, and **Instance name**.

### Python Script
The following Python script uses `boto3` to create the EC2 instance, security group, key pair, and instance tags:

```python
import boto3 as bt
import os

# Constants
GroupName = '24188516-sg-2'
KeyName = '24188516-key-2'
InstanceName = '24188516-vm-2'

ec2 = bt.client('ec2')

# 1. Create security group
step1_response = ec2.create_security_group(
    Description="security group for development environment",
    GroupName=GroupName
)

# 2. Authorize SSH inbound rule
step2_response = ec2.authorize_security_group_ingress(
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

# 3. Create key pair
step3_response = ec2.create_key_pair(KeyName=KeyName)
PrivateKey = step3_response['KeyMaterial']

# Save key pair to a file
with open(f'{KeyName}.pem', 'w') as file:
    file.write(PrivateKey)

# Grant file permission to the private key
os.chmod(f'{KeyName}.pem', 0o400)

# 4. Create EC2 instance
step4_response = ec2.run_instances(
    ImageId='ami-07a0715df72e58928',
    SecurityGroupIds=[GroupName],
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName=KeyName
)

# Retrieve the Instance ID
InstanceId = step4_response['Instances'][0]['InstanceId']

# 5. Create a tag for the instance
step5_response = ec2.create_tags(
    Resources=[InstanceId],
    Tags=[{'Key': 'Name', 'Value': InstanceName}]
)

# 6. Get the public IP address of the instance
step6_response = ec2.describe_instances(InstanceIds=[InstanceId])
public_ip_address = step6_response['Reservations'][0]['Instances'][0]['PublicIpAddress']

# Print all responses
print(f"{step1_response}\n{step2_response}\n{PrivateKey}\n{InstanceId}\n{step5_response}\n{public_ip_address}\n")
```

### Code Explanation
1. **Security Group Creation**: We first create a security group with the name `24188516-sg-2` to manage inbound and outbound rules.
2. **SSH Authorization**: An inbound rule is added to allow SSH access (TCP on port 22) for all IPs (`0.0.0.0/0`).
3. **Key Pair Creation**: We generate a key pair (`24188516-key-2`), save the private key in a `.pem` file, and set the correct file permissions for security.
4. **Instance Creation**: This step launches a `t3.micro` EC2 instance with the AMI ID `ami-07a0715df72e58928` and attaches the security group and key pair.
5. **Tagging the Instance**: The instance is tagged with the name `24188516-vm-2` to identify it.
6. **Retrieving the Public IP**: After the instance is created, the public IP address is retrieved for SSH access.

### Output and Results
Once the script is executed, the responses from each step are printed, showing the security group creation, key pair, instance ID, and public IP address.

![Script Output](http://127.0.0.1/assets/lab2-10.png)

Let's verify the created instance in the AWS console:

![AWS Console Instance](http://127.0.0.1/assets/lab2-11.png)

## Use Docker Inside a Linux OS

### 1. Install Docker
To install Docker, we first run the following command to install the necessary packages for the Docker service:
```bash
sudo apt install docker.io -y
```

### 2. Start the Docker Service
After installation, we start the Docker service with:
```bash
sudo systemctl start docker
```

### 3. Enable Docker to Start on Boot
To ensure Docker starts automatically at boot, we enable it using:
```bash
sudo systemctl enable docker
```

![Docker Installation](http://127.0.0.1/assets/lab2-12.png)

### 4. Check Docker Version
After the Docker service is installed and enabled, we can verify that Docker is working properly by checking its version:
```bash
docker --version
```

This command prints out the installed version of Docker, confirming that it's functional.

![Docker Version Check](http://127.0.0.1/assets/lab2-13.png)

### 5. Build and Run an `httpd` Container
Next, we create an HTML file to be served via an Apache HTTP server running inside a Docker container. The file `index.html` is located inside the `html` directory and contains the following content:
```html
  <html>
    <head></head>
    <body>
      <p>Hello, World!</p>
    </body>
  </html>
```

#### Create a Dockerfile
Outside the `html` directory, we create a `Dockerfile` with the following content:
```Dockerfile
FROM httpd:2.4
COPY ./html/ /usr/local/apache2/htdocs/
```

This Dockerfile specifies that we are using Apache HTTP Server version 2.4 and that the contents of the `html` folder should be copied to the appropriate directory inside the Docker container (`/usr/local/apache2/htdocs/`).

#### Add User to Docker Group
We add our username (`liudayubob`) to the Docker group to grant permission to manage Docker containers, then reboot the Ubuntu console:
```bash
sudo usermod -a -G docker liudayubob
```

#### Build the Docker Image
To build the Docker image, we navigate to the current directory (where the `Dockerfile` and `html` folder are located) and run the following command:
```bash
docker build -t my-apache2 .
```

This command builds the image and tags it as `my-apache2`.

![Docker Build](http://127.0.0.1/assets/lab2-14.png)

#### Run the Docker Container
Now, we run the image using the following command:
```bash
docker run -p 80:80 -dit --name my-app my-apache2
```

This command maps the host machine's port **80** to the Docker container's port **80**, runs the container in detached mode with the name `my-app`, and uses the `my-apache2` image.

![Docker Run](http://127.0.0.1/assets/lab2-15.png)

#### Access the Hosted HTML Page
Open a browser and access `http://localhost` or `http://127.0.0.1`. The HTML page is now live and displays "Hello, World!"

![Docker Webpage](http://127.0.0.1/assets/lab2-16.png)

### 6. Other Docker Commands

#### Check Running Containers
To list all running containers, use:
```bash
docker ps -a
```

This command displays the properties of the running containers, such as **Container ID**, **STATUS**, **PORTS**, the assigned container name, and the image used.

![Docker ps -a](http://127.0.0.1/assets/lab2-17.png)

#### Stop and Remove the Container
To stop and remove the running container, use the following commands:
```bash
docker stop my-app
docker rm my-app
```

These commands stop the `my-app` container and then remove it from the system.

<div  style="page-break-after: always;"></div>


# Lab 3

### 1. Preparation
We begin by creating the required files and directories. The following file structure contains three files: `cloudstorage.py`, `rootfile.txt`, and `subfile.txt`.

![File Structure](http://127.0.0.1/assets/lab2-18.png)

### 2. Save to S3 by Updating `cloudstorage.py`
The `cloudstorage.py` script is modified to create an S3 bucket named `24188516-cloudstorage` if it doesn’t already exist. The script then traverses through all directories and subdirectories in the root directory and uploads any discovered files to the S3 bucket.

```python
import os
import boto3

ROOT_DIR = '.'
ROOT_S3_DIR = '24188516-cloudstorage'
s3 = boto3.client("s3")

bucket_config = {'LocationConstraint': 'eu-north-1'}

def upload_file(folder_name, file, file_name):
    file_key = os.path.join(folder_name, file_name).replace("\\", "/")
    s3.upload_file(file, ROOT_S3_DIR, file_name)  # file path, bucket name, key
    print(f"Uploading {file}")

# Main program
try:
    # Create bucket if not there
    response = s3.create_bucket(
        Bucket=ROOT_S3_DIR,
        CreateBucketConfiguration=bucket_config
    )
    print(f"Bucket created: {response}")
except Exception as error:
    print(f"Bucket creation failed: {error}")
    pass

# Traverse directory and upload files
for dir_name, subdir_list, file_list in os.walk(ROOT_DIR, topdown=True):
    if dir_name != ROOT_DIR:
        for fname in file_list:
            upload_file(f"{dir_name[2:]}/", f"{dir_name}/{fname}", fname)

print("done")
```

The method `s3.upload_file()` accepts three parameters: **File path**, **Bucket name**, and **File key**. We concatenate both the *folder_name* and *file_name* to form the file key, ensuring the file is uploaded with the same directory structure as our local machine.

![S3 Upload](http://localhost/assets/lab2-19.png)

### 3. Restore from S3
We create a new program, `restorefromcloud.py`, to restore files from the S3 bucket and write them to the appropriate directories. The program uses `s3.list_objects_v2` to list all files in the S3 bucket and their attributes (e.g., **Key, Name**). 

We join the local **ROOT_TARGET_DIR** with the **Key** to form the local file path. If the local directory doesn't exist, we create it using `os.makedirs()`. Finally, we download each file from the S3 bucket using `s3.download_file()` with the parameters **Bucket**, **Key**, and **Filename**.

```python
import os
import boto3

ROOT_TARGET_DIR = '.'  # Root directory where files will be restored
ROOT_S3_DIR = '24188516-cloudstorage'
s3 = boto3.client("s3")

def download_file(s3_key, local_file_path):
    local_dir = os.path.dirname(local_file_path)
    
    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        print(f"Creating directory {local_dir}")
        os.makedirs(local_dir)

    # Download the file
    s3.download_file(ROOT_S3_DIR, s3_key, local_file_path)
    print(f"Downloading {s3_key} to {local_file_path}")

# Main program
# List all objects in the S3 bucket
objects = s3.list_objects_v2(Bucket=ROOT_S3_DIR)

if 'Contents' in objects:
    for obj in objects['Contents']:
        s3_key = obj['Key']
        local_file_path = os.path.join(ROOT_TARGET_DIR, s3_key).replace("/", os.path.sep)
        
        # Download the file from S3 to the corresponding local path
        download_file(s3_key, local_file_path)
else:
    print("No objects found in the bucket.")
    pass

print("done")
```

This script traverses the S3 bucket, restoring files to the local directory in the same structure they were uploaded.

![S3 Restore](http://localhost/assets/lab2-20.png)



### 4. Write Information About Files to DynamoDB

#### 1. Install DynamoDB
First, we create and navigate into the `dynamodb` directory. We then install **JRE** and the **DynamoDB** package, extracting the necessary files for local use. Once extracted, we have the compiled Java code `DynamoDBLocal.jar` and a folder containing libraries `DynamoDBLocal_lib`, which we use to run a local DynamoDB instance.

```bash
mkdir dynamodb
cd dynamodb

# Install JRE
sudo apt-get install default-jre

# Download DynamoDB package
wget https://s3-ap-northeast-1.amazonaws.com/dynamodb-local-tokyo/dynamodb_local_latest.tar.gz

# Extract DynamoDB
tar -zxvf dynamodb_local_latest.tar.gz
```

![DynamoDB Extraction](http://localhost/assets/lab2-21.png)

Next, we start the DynamoDB instance locally using **JRE**. We specify the port as **8001** since **8000** is already in use. The `-sharedDb` flag creates a single database file, `_shared-local-instance.db`, which is accessed by all programs connecting to DynamoDB.

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar –sharedDb -port 8001
```

![Start DynamoDB](http://localhost/assets/lab2-22.png)

#### 2. Create a Table in DynamoDB
We then create a Python script, `createtable.py`, to define a table named `CloudFiles` in DynamoDB. The table uses `userId` as the partition key and `fileName` as the sort key. We define the keys using `KeyType` (`HASH` for partition key and `RANGE` for sort key), while `AttributeName` and `AttributeType` specify the attributes' names and types.

Although DynamoDB is schema-free, meaning attributes like `path`, `lastUpdated`, `owner`, and `permissions` don't need to be predefined, we include them for future use when inserting items into the table.

Here’s the table schema:
```python
# Database schema
CloudFiles = {
    'userId',
    'fileName',
    'path',
    'lastUpdated',
    'owner',
    'permissions'
}
```

Here’s the script to create the table:
```python
# createtable.py
import boto3

def create_db_table():
    # Initialize DynamoDB service instance
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8001")
    
    table = dynamodb.create_table(
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
                'AttributeType': 'S'  # String type
            },
            {
                'AttributeName': 'fileName',
                'AttributeType': 'S'  # String type
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    
    print("Table status:", table.table_status)

if __name__ == '__main__':
    create_db_table()
```

This script connects to the local DynamoDB instance running on port **8001** and creates the `CloudFiles` table with the specified schema. It prints the table's status after creation.

![Create DynamoDB Table](http://localhost/assets/lab2-23.png)



### 3. Write Data into the `CloudFiles` Table
In this step, we write data into the `CloudFiles` table. First, we use `s3.list_objects_v2()` to list all files in the `24188516-cloudstorage` bucket. The output contains attributes such as **Key** and **LastModified**. To retrieve additional information like **Owner** and **Permissions**, we make a separate call to `s3.get_object_acl()`, which provides these details under the **Grants** and **Owner** attributes.

After extracting all necessary attributes, we use `dynamodb_table.put_item()` to insert each object into the DynamoDB table. Since the region is `eu-north-1`, we populate the `owner` field with the owner's ID.

Here’s the script:

```python
# writetable.py
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
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' in objects:
        for obj in objects['Contents']:
            # Get access control list for owner and permission information
            obj_acl = s3.get_object_acl(Bucket=BUCKET_NAME, Key=obj['Key'])
            files.append({**obj, **obj_acl})
    
    return files

def extract_file_attributes(file):
    # Extract attributes of a file
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
    # List all files in the bucket and write them to the DynamoDB table
    try:
        files = list_files()
        
        # Iterate through each file
        for file in files:
            # Extract attributes for the file
            file_attributes = extract_file_attributes(file)
            
            # Write the attributes to DynamoDB
            db_res = dynamodb_table.put_item(Item=file_attributes)
            print(f"Inserted {file_attributes['fileName']} into DynamoDB")
    
    except Exception as error:
        print(f"Database write operation failed: {error}")
        pass

if __name__ == '__main__':
    write_to_table()
```

This script performs the following:
1. Lists all files in the S3 bucket using `s3.list_objects_v2`.
2. Retrieves owner and permission information using `s3.get_object_acl`.
3. Extracts file attributes like `userId`, `fileName`, `path`, `lastUpdated`, `owner`, and `permissions`.
4. Inserts each file's attributes into the DynamoDB table using `put_item()`.

![DynamoDB Write](http://localhost/assets/lab2-24.png)

### 4. Print and Destroy the `CloudFiles` Table

#### Print the Table
We use the AWS CLI to scan and print the contents of the `CloudFiles` table. The following command retrieves all items in the table and displays them:

```bash
aws dynamodb scan --table-name CloudFiles --endpoint-url http://localhost:8001
```

This command prints the table structure, showing the data we inserted in the previous step.

![DynamoDB Scan](http://localhost/assets/lab2-25.png)

#### Destroy the Table
To delete the `CloudFiles` table, we use the following AWS CLI command:

```bash
aws dynamodb delete-table --table-name CloudFiles --endpoint-url http://localhost:8001
```

This command deletes the table, removing all data and schema. Only the defined schema (partition key and sort key) will be printed before deletion.

![DynamoDB Delete Table](http://localhost/assets/lab2-26.png)

<div  style="page-break-after: always;"></div>


# Lab 4
## Apply a Policy to Restrict Permissions on Bucket

### 1. Write a Python Script
In this lab, we apply an access permission policy to the S3 bucket `24188516-cloudstorage` created in the previous lab. The policy restricts access to this bucket, allowing only the user with the username `24188516@student.uwa.edu.au` to access the contents. 

The policy is defined as a JSON document, where:
- **Sid** is a unique identifier for the policy statement.
- **Effect** is set to `"DENY"`, meaning the action is denied if the condition is met.
- **Action** is `"s3:*"`, meaning all S3 actions are denied.
- **Resource** specifies all objects in the `24188516-cloudstorage` bucket.
- **Condition** checks if the `aws:username` is not `24188516@student.uwa.edu.au`. If this condition is true, access is denied.

Here’s the bucket policy in JSON format:

```json
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
				"aws:username": "24188516@student.uwa.edu.au"
			}
		}
	}
}
```

This JSON policy ensures that any user attempting to access the bucket, who is not `24188516@student.uwa.edu.au`, will be denied all actions related to S3.

#### Python Script to Apply the Policy
Since the policy parameter in `s3.put_bucket_policy()` only accepts a JSON string, we load the JSON policy from `bucketpolicy.json`, convert it into a string using `json.dumps()`, and then apply it to the bucket using `s3.put_bucket_policy()`.

Here’s the Python script to apply the policy:

```python
# addpolicy.py
import boto3
import json

BUCKET_NAME = '24188516-cloudstorage'

# Create an S3 instance
s3 = boto3.client('s3')

def apply_bucket_policy():
    # Import the policy from the JSON file
    with open('bucketpolicy.json', 'r') as policy_file:
        policy = json.load(policy_file)
    
    # Convert the policy to a JSON string
    policy_string = json.dumps(policy)

    # Apply the policy to the bucket
    response = s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=policy_string)
    print("Policy applied!", response)

if __name__ == '__main__':
    apply_bucket_policy()
```

This script does the following:
1. Reads the JSON policy from `bucketpolicy.json`.
2. Converts the policy into a string format.
3. Applies the policy to the S3 bucket using `s3.put_bucket_policy()`.

![Applying S3 Bucket Policy](http://localhost/assets/lab4-1.png)

### Key Points:
- **Policy Application**: The policy restricts access to the bucket based on the requesting user's username.
- **Policy Format**: The policy is written in JSON format and applied to the bucket using Python and the `boto3` library.

### 2. Check Whether the Script Works
After applying the bucket policy, we test to ensure that the policy is working as intended.

#### Verify the Policy Using AWS CLI
To check whether the policy has been applied to the `24188516-cloudstorage` bucket, we use the following AWS CLI command:

```bash
aws s3api get-bucket-policy --bucket 24188516-cloudstorage --query Policy --output text
```

This command retrieves the policy attached to the S3 bucket and outputs it in plain text. The expected output is the JSON policy document we applied earlier.

![Policy Check with AWS CLI](http://localhost/assets/lab4-2.png)

#### Visual Confirmation via AWS Console
Next, we navigate to the AWS console to visually confirm that the policy is in place for the `24188516-cloudstorage` bucket. The console should display the same policy, with the conditions we set for restricting access based on the username.

![Policy Check in AWS Console](http://localhost/assets/lab4-3.png)

#### Test Denied Access with Incorrect Username
To test whether the policy is correctly restricting access, we deliberately alter the username in the policy. For example, we change the username condition to only allow access to `12345678@student.uwa.edu.au`, effectively denying access to the current user `24188516@student.uwa.edu.au`.

As expected, when trying to access the bucket resources under the user `24188516@student.uwa.edu.au`, the access is denied.

![Denied Access](http://localhost/assets/lab4-4.png)
![Access Denied](http://localhost/assets/lab4-5.png)

### Key Points:
- **AWS CLI Check**: We use the AWS CLI to retrieve and verify the bucket policy in plain text.
- **Console Check**: We visually confirm the policy through the AWS console.
- **Testing Access Control**: By modifying the policy, we test and confirm that access is denied for unauthorized users.



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
- For the file_content,  it concatenates the **nonce, tag, and ciphertext** in this exact order into a single byte sequence (`file_body`). **nonce** is a unique value generated to make sure the resulting ciphertext will be different and avoid similar issue to **Hash Collision**.
```
# Encrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(file_content) #  extract the ciphertext and tag from the encrypted content
    encrypt_file_key = f"{file_key}.encrypted"

    # Concatenate the nonce, tag, and the ciphertext
    file_body = cipher.nonce + tag + cipher_text
```

- For the decryption part, we need to first extract **nonce, tag, and ciphertext** from the **file_body**. _Nonce_ is the first 16 bytes of the string, _tag_ is the next 16 bytes and _cipher_text _ is the remaining part of the actual encrypted file content, starting from byte 32 onward. 
- We need extracted **nonce** to create a cipher object with the original encryption setup. `cipher.decrypt_and_verify()` decrypts the ciphertext and verifies its integrity using the extracted **tag**
```
    # Parse the nonce, tag, and the ciphertext from the file content
    nonce = file_body[:16]  # 16 bytes for the nonce
    tag = file_body[16:32]  # 16 bytes for the tag
    cipher_text = file_body[32:] # The rest of the file content is the ciphertext

    # Decrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    plain_text = cipher.decrypt_and_verify(cipher_text, tag)
    file_body = plain_text.decode('utf-8') #convert plain text bytes to a regular string
```

3. See in actions
Now lets run `python3 cryptwithpycryptodome.py` and see the new approach in action. You can tell that the encrypted contents are different from **[4]** before the encryption key is different. 
![enter image description here](http://localhost/assets/lab4-13.png)
![enter image description here](http://localhost/assets/lab4-10.png)
![enter image description here](http://localhost/assets/lab4-11.png)

## Answer the following question (Marked)

```
What is the performance difference between using KMS and using the custom solution?
```
```
Answer:
I think KMS outperforms in its ease of maintainence and high scalability.
It offers automated key management so we don't need to manually save our keys.
KMS is also highly scalable because they are based on cloud infrastructure, which is critical under significant workload.
**PyCryptodome** is better for its extensibility and low internet overhead. PyCryptodome offers more room of customization with more cryptography algorithms and combinations with different configurations.
It doesn't rely on API calls which are subject to connectivetity and rate limits.
However since encryption/decrption are done on local machine, it doesn't scale well with high workload.

```
<div  style="page-break-after: always;"></div>

# Lab 5
## Application Load Balancer

### [1] Create 2 EC2 instances & Add Application Load Balancer
In the first part to create EC2 instances, we can replicate our code from **lab2** as an entry point. To differentiate some ARNs that were already declared in **lab2**, some resource names are hypenated with suffix "lab5" at the end, for example:
```
GroupName = '24188516-sg-lab5'
KeyName = '24188516-key-lab5'
```
The only difference is that we need to create EC2 instances and specify their separated availbility zones (subnet). This can be done by using `ec2.describe_subnets()` to fetch the subnets in each dedicated availablity zones and add the parameter **SubnetId** when doing `ec2.run_instances(SubnetId=SubnetId)`.

Then we will create *load balancer* and *target group* step by step
 - Create load balancer: Use `elbv2.create_load_balancer()` with our choosen **Subnets**, created **SecurityGroups**, etc.
 - Create target group: Use `ec2.describe_vpcs()` to find the vpc that will host our instances and then use `elbv2.create_target_group()` with **Protocol**, **Port**, **VpcId**, etc.
- Register instances as targets: Use `elbv2.register_targets()` with **TargetGroupArn** (return from `elbv2.create_target_group()`),**Targets** (Id as **InstanceId**), etc.
- Add a listener to forward traffic from **port 80** to the **target group** (EC2 instance): Use `elbv2.create_listener()` with **LoadBalancerArn** (return from `elbv2.create_load_balancer()`), **DefaultActions** as **forward** to the **TargetGroupArn**, etc.

This is the full code script that perform the actions above.
```
import boto3 as bt
import os

GroupName = '24188516-sg-lab5'
KeyName = '24188516-key-lab5'
InstanceName1 = '24188516-vm1'
InstanceName2 = '24188516-vm2'
LoadBalancerName = '24188516-elb'
TargetGroupName = '24188516-tg'

# Initialize EC2 and ELBv2 clients
ec2 = bt.client('ec2', region_name='eu-north-1')
elbv2 = bt.client('elbv2')

# 1. Create security group
step1_response = ec2.create_security_group(
    Description="Security group for lab5 environment",
    GroupName=GroupName
)

# 2. Authorize SSH (port 22) and HTTP (port 80) inbound rules
step2_response = ec2.authorize_security_group_ingress(
    GroupName=GroupName,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

# 3. Create key-pair
step3_response = ec2.create_key_pair(KeyName=KeyName)
PrivateKey = step3_response['KeyMaterial']
## Save key-pair
with open(f'{KeyName}.pem', 'w') as file:
    file.write(PrivateKey)
## Grant file permission
os.chmod(f'{KeyName}.pem', 0o400)

# 4. Get two of subnets in availability zones
step4_response = ec2.describe_subnets()['Subnets']
Subnets = [subnet['SubnetId'] for subnet in step4_response[:2]]

# 5. Create instances in these two availability zones
Instances = []
for idx, SubnetId in enumerate(Subnets):
    InstanceName = f"24188516-vm{idx + 1}"
    step5_response = ec2.run_instances(
        ImageId='ami-07a0715df72e58928',
        SecurityGroupIds=[step1_response['GroupId']],
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName=KeyName,
        SubnetId=SubnetId
    )
    InstanceId = step5_response['Instances'][0]['InstanceId']
    Instances.append(InstanceId)
    
    # Tag instance with the appropriate name
    ec2.create_tags(
        Resources=[InstanceId],
        Tags=[
            {
                'Key': 'Name',
                'Value': InstanceName
            }
        ]
    )

# 6. Create application load balancer
step6_response = elbv2.create_load_balancer(
    Name=LoadBalancerName,
    Subnets=Subnets,
    SecurityGroups=[step1_response['GroupId']],
    Scheme='internet-facing',
    Type='application'
)
LoadBalancerArn = step6_response['LoadBalancers'][0]['LoadBalancerArn']

# 7. Create target group
VpcId = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
step7_response = elbv2.create_target_group(
    Name=TargetGroupName,
    Protocol='HTTP',
    Port=80,
    VpcId=VpcId,
    TargetType='instance'
)
TargetGroupArn = step7_response['TargetGroups'][0]['TargetGroupArn']

# 8. Register instances as targets
elbv2.register_targets(
    TargetGroupArn=TargetGroupArn,
    Targets=[{'Id': InstanceId} for InstanceId in Instances]
)

# 9. Create a listener for the load balancer
elbv2.create_listener(
    LoadBalancerArn=LoadBalancerArn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[{
        'Type': 'forward',
        'TargetGroupArn': TargetGroupArn
    }]
)

# Printouts
print(f"Instance IDs: {Instances}")
print(f"Load Balancer ARN: {LoadBalancerArn}")
print(f"Target Group ARN: {TargetGroupArn}")
```
After the execution, go to the console and confirm our *load balancer* and *target group* created.
![enter image description here](http://localhost/assets/lab5-2.png)
![enter image description here](http://localhost/assets/lab5-3.png)

Record the public IPv4 addresses for both instances created.
![enter image description here](http://localhost/assets/lab5-4.png)

### [3] SSH to our instances
We need to install apache and start the application to see our load balancer in action.
We already stored the generated private key as **24188516-key-lab5.pem** for both EC2 instances in step [3].
Bacause I use Putty on Windows OS, first we need to use PuttyGen to convert pem key file to ppk format for later ssh actions.
![enter image description here](http://localhost/assets/lab5-5.png)

Now configure the authentication credentials and host on Putty with our converted keys and Ip addresses we recorded from the last step.
![enter image description here](http://localhost/assets/lab5-6.png)
![enter image description here](http://localhost/assets/lab5-7.png)

As you can see, now we are logged in. 
![enter image description here](http://localhost/assets/lab5-8.png)

### [4] Install apache & Access results using IP addresses

First, let's update each instance and install apache2 in each instance:
```
sudo apt-get update
sudo apt install apache2
```
![enter image description here](http://localhost/assets/lab5-9.png)

Now, edit the `<title>` and `</title>` tags inside the `/var/www/html/index.html` file to show the instance name.
```
sudo vi /var/www/html/index.html

# index.html
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Hello, this is VM1!</title>
<style type="text/css" media="screen">
```
![enter image description here](http://localhost/assets/lab5-10.png)

Now we can go the the IP addresses allocated to each instance and see that the new title names are applied
![enter image description here](http://localhost/assets/lab5-11.png)
![enter image description here](http://localhost/assets/lab5-12.png)

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExNjQ1NTY0MjEsLTYyNDM0Mzg3Nyw3Mz
UyMDY5MjksLTEwMjQyMDU0NCwtMTQyMjM0NzE4MCwzNzM4OTQz
NTAsLTIwNTAwMTIxMzIsLTk0ODE4NzQsNTYwODU5NDE2LDE0Mz
YzODQzNjYsLTkxMTY0MDYyMCwtMjA4ODc0NjYxMl19 
-->
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTgzNjE3OTYxMiw1MzMxNzMzODYsNDMwNz
U3MTQ5LC0xMzIyNDEyNDQ5LDM5OTY2NTY5MiwtMTE4NzA3MTgw
OSwxNDgzNTI2NDIzLDk0NTcyNzY0MSwxNTMzMDQ4NTQzLDU0MT
c0ODQ0NCwxMzQ3MTMxMDA4LDEyMTQ5ODc3NzEsLTE1NDk4NzEz
OTUsLTEyNTEzNjE0MjcsLTkyODM5Mzk3MSwtMTk1NzEyOTU2LD
Y5Njk3MjE1NiwtMTc4NDE2NTE1OCwtMTc2Njk4OTkzNiwtMTA4
NzA5MjY0MF19
-->