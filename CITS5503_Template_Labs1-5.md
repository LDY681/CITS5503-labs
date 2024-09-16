
<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">
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

Since upgrading packages involves modifying the system, administrative privileges are required. This is why we prefix the command with `sudo`. 
-  **`apt update`** updates the package lists from **Apt** package management tool. These package lists contain references to the latest versions of packages. 
-  **`apt upgrade`** upgrades all installed packages to their latest versions based on the information fetched from the update command, `-y` automatically answers **YES** to any prompts that might appear during the upgrade process.


#### Verify Python Version
To confirm that Python is installed and check the version, use the following command:

```bash
python3 -V
```

- **`python3`**: This specifies that we are checking the version of Python 3.x.
- **`-V`**: Outputs the installed Python version.

The output verifies that Python 3.10.12 is installed.

![Check Python Version](http://127.0.0.1/assets/lab1-6.png)

#### Install pip3
To install and manage Python libraries, use **pip**. Install it with:

```bash
sudo apt install -y python3-pip
```

- **`python3-pip`**: Installs pip for Python 3 specifically.

Once installed, you can use `pip3` to install third-party Python packages

![Installing pip3](http://127.0.0.1/assets/lab1-7.png)

### 2. Install AWS CLI
To interact with AWS services from the command line, we use the AWS CLI (Command Line Interface). Install and upgrade it to the latest version using:

```bash
pip3 install awscli --upgrade
```

- **`awscli`**: This installs the AWS Command Line Interface, enabling us to manage AWS services like EC2, S3, and more directly from the terminal.
- **`--upgrade`**: Ensures that if an older version of AWS CLI is already installed, it will be replaced with the latest version, which includes new features, updates, and security patches.

Once installed, we can execute AWS CLI commands to interact with various AWS resources such as EC2, S3, etc.

![Install AWS CLI](http://127.0.0.1/assets/lab1-8.png)

### 3. Configure AWS CLI
After installation, configure the AWS CLI to connect to our Amazon EC2 instance. This is done by entering your credentials **Access Key ID, Secret Access Key, Region** using the following command:
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
To verify that our AWS CLI is configured correctly and connected to the AWS environment, we run the following command to list the available regions in our AWS account:

```bash
aws ec2 describe-regions --output table
```

- **`aws ec2 describe-regions`**: This command queries the AWS EC2 service to list all available regions where AWS services are provided.
- **`--output table`**: Formats the output in a readable table structure, making it easier to view and interpret the region data.

This command allows us to verify that we are connected to AWS, and the output should display a list of regions in a structured table.

![AWS Region Table](http://127.0.0.1/assets/lab1-11.png)



### 2. Test the Python Environment
After confirming that the AWS CLI is working correctly, we now test the Python environment using **`boto3`**, the AWS SDK for Python. This allows us to interact with AWS services programmatically through Python.

The following Python code connects to the AWS EC2 service and retrieves the available regions, similar to the CLI test but now within the Python environment:

```python
python3
>>> import boto3
>>> ec2 = boto3.client('ec2')
>>> response = ec2.describe_regions()
>>> print(response)
```

- **`import boto3`**: Imports the **`boto3`** library, which is used to interact with AWS services via Python.
- **`boto3.client('ec2')`**: Initializes a client for the EC2 service, allowing us to make requests to EC2, such as querying regions, starting instances, etc.
- **`ec2.describe_regions()`**: This method queries the EC2 service to retrieve a list of available AWS regions. It returns the data in JSON format.
- **`print(response)`**: Outputs the result, which contains details about the available regions, in a JSON structure.

This code verifies that our Python environment is correctly set up and able to interact with AWS services via `boto3`.

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
After running the Python script, the results are printed in a table format. The table shows the available AWS regions along with the corresponding **Endpoint**, **RegionName**, and **OptInStatus**.

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

- **Endpoint**: Indicates a public URL of the AWS service (EC2) for each region. It’s the endpoint through which API calls are routed for that specific region.
- **RegionName**: Represents the region code for each AWS region. In the future labs, we will be using `eu-north-1` for the European North region .
- **OptInStatus**: Shows the status of whether a region requires users to opt-in before using it. `opt-in-not-required` means that the region is generally available for all AWS users.

This table helps verify the connection to AWS and confirms that the Python environment is correctly configured to retrieve information from AWS services.

<div  style="page-break-after: always;"></div>

# Lab 2

## Create an EC2 Instance Using AWS CLI


### 1. Create a Security Group

We begin by creating a security group with a unique name based on our student number, `24188516-sg`. A security group acts as a virtual firewall for our EC2 instances, controlling inbound and outbound traffic.

The following command creates the security group:

```bash
aws ec2 create-security-group --group-name 24188516-sg --description "security group for development environment"
```

#### Key Parameters:
- **`--group-name`**: Specifies the name of the security group. In this case, we use `24188516-sg` to uniquely identify the group based on our student number.
  
- **`--description`**: Provides a human-readable description of the security group’s purpose. Here, we describe it as "security group for development environment" to indicate the group will be used for development purposes.

Once executed, this command will create the security group and return the **GroupId**, which is a unique identifier for the newly created security group. The **GroupId** is important because it will be used in future commands when modifying or referencing the security group.

![Create Security Group](http://127.0.0.1/assets/lab2-1.png)

The screenshot shows the output of the command, displaying the **GroupId** for the newly created security group.



### 2. Authorize Inbound Traffic for SSH

Now that the security group is created, we need to add a rule to allow inbound SSH traffic. This is necessary to enable secure access to our EC2 instances using the SSH protocol on port 22.

The following command authorizes inbound traffic for SSH:

```bash
aws ec2 authorize-security-group-ingress --group-name 24188516-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
```

#### Key Parameters:
- **`--group-name`**: Specifies the name of the security group to which the rule will be added. In this case, we are adding the rule to the `24188516-sg` security group created in the previous step.
- **`--protocol`**: Defines the protocol for the rule. Here, we use **`tcp`** to specify the Transmission Control Protocol, which is the standard protocol used for SSH.
- **`--port`**: Specifies the port number on which the traffic will be allowed. In this case, we set it to **`22`**, the default port for SSH connections.
- **`--cidr`**: Defines the range of IP addresses allowed to access the instance via SSH. **`0.0.0.0/0`** means that traffic is allowed from any IP address, giving unrestricted access to SSH from anywhere in the world. This is common for testing purposes but should be restricted for production environments.

Once executed, this command creates a rule allowing SSH access on port 22, and the response confirms the rule creation by displaying the details of the newly added rule.

![Authorize Inbound Traffic](http://127.0.0.1/assets/lab2-2.png)

The screenshot shows the successful creation of the security rule allowing inbound SSH traffic to the security group.


### 3. Create a Key Pair

To securely connect to the EC2 instance, we generate a public and private key pair. The private key will be used to authenticate SSH connections, while the public key is associated with the EC2 instance. This step is crucial for securing the private key and ensuring that it can be used for SSH connections without exposing it to others.

The following command creates a key pair:

```bash
aws ec2 create-key-pair --key-name 24188516-key --query 'KeyMaterial' --output text > 24188516-key.pem
```

#### Key Parameters:
- **`--key-name`**: Specifies the name of the key pair being created. In this case, the key pair is named `24188516-key`, which is based on our student number for identification.
- **`--query 'KeyMaterial'`**: This option extracts the private key (key material) from the response and outputs it as plain text. The key material is the private part of the key pair, which is required to authenticate SSH sessions.
- **`--output text`**: Specifies that the output format should be plain text (instead of JSON). The output is redirected to a file using the `>` operator, which saves the private key as `24188516-key.pem`.

#### Set Permissions for the Key:
After the key is generated, we ensure it has the correct permissions using the following command:

```bash
chmod 400 24188516-key.pem
```

- **`chmod 400`**: This changes the file’s permissions to **read-only** for the owner. It ensures that only the owner of the file can read it, which is necessary to secure the key and prevent unauthorized access.

Below are the outputs after successfully creating the key and setting the appropriate permissions:

![Key Pair Creation](http://127.0.0.1/assets/lab2-3.png)
![Permission Change](http://127.0.0.1/assets/lab2-4.png)


### 4. Create the Instance
Now, we create an EC2 instance using the `aws ec2 run-instances` command. Since my student number is `24188516`, create an EC2 instance in the `eu-north-1` region.

```bash
aws ec2 run-instances --image-id ami-07a0715df72e58928 --security-group-ids 24188516-sg --count 1 --instance-type t3.micro --key-name 24188516-key --query 'Instances[0].InstanceId'
```

> At the time of running the lab, the **t2.micro** instance type was not available, so we switched to **t3.micro**. The instance was successfully created with the instance ID `i-0553e2ea0492e1c73`.

#### Key Parameters:
- **`--image-id`**: Specifies the Amazon Machine Image (AMI) ID to be used for the instance. In this case, `ami-07a0715df72e58928` is used, refers to a pre-configured image for this class.
- **`--security-group-ids`**: Links the instance to the previously created security group (`24188516-sg`). This security group defines the allowed inbound and outbound traffic rules, including SSH access on port 22.
- **`--count`**: Specifies that only one instance will be created. This flag allows you to create multiple instances simultaneously if needed.
- **`--instance-type`**: Defines the type of EC2 instance to launch. Due to limitations at the time, **t3.micro** was chosen instead of **t2.micro**.
- **`--key-name`**: Specifies the name of the key pair (`24188516-key`) to associate with the instance. This key will be used to securely access the instance via SSH.
- **`--query 'Instances[0].InstanceId'`**: This extracts and displays the **InstanceId** of the newly created EC2 instance.

Once the command is executed, the instance is successfully created, and the **InstanceId** is displayed. In this case, the instance ID returned is `i-0553e2ea0492e1c73`.

![Create EC2 Instance](http://127.0.0.1/assets/lab2-6.png)
![Instance ID](http://127.0.0.1/assets/lab2-5.png)

The screenshots show the successful creation of the EC2 instance and the returned **InstanceId**.

### 5. Add a Tag to the Instance
Now that we have the instance ID `i-0553e2ea0492e1c73`, we will add a tag to name the instance. The tag key will be `Name`, and the value will be our student number followed by `-vm` to uniquely identify the instance as `24188516-vm`.

```bash
aws ec2 create-tags --resources i-0553e2ea0492e1c73 --tags Key=Name,Value=24188516-vm
```

#### Key Parameters:
- **`--resources`**: Specifies the ID of the resource to tag, in this case, the instance ID `i-0553e2ea0492e1c73`.
- **`--tags`**: Defines the key-value pair for the tag. Here, the key is `Name`, and the value is `24188516-vm`, which labels the instance for identification purposes.

Once the command is executed, the instance will be tagged with `24188516-vm`, making it easier to identify in the AWS console.

### 6. Get the Public IP Address
To retrieve the public IP address of the instance, we use the `describe-instances` command. The query extracts only the `PublicIpAddress` from the instance details:

```bash
aws ec2 describe-instances --instance-ids i-0553e2ea0492e1c73 --query 'Reservations[0].Instances[0].PublicIpAddress'
```

#### Key Parameters:
- **`--instance-ids`**: Specifies the instance ID, which is `i-0553e2ea0492e1c73` in this case.
- **`--query`**: Limits the output to the `PublicIpAddress` of the instance, providing the required IP address for SSH access.

This IP address is crucial for connecting to the instance via SSH.

![Public IP Address](http://127.0.0.1/assets/lab2-7.png)

### 7. Connect to the Instance via SSH
Now, we connect to the instance using the public IP address `16.171.151.20` via SSH. We use the previously generated `.pem` file to authenticate:

```bash
ssh -i 24188516-key.pem ubuntu@16.171.151.20
```

#### Key Parameters: 
- **`-i`**: Specifies the identity file (private key) to use for SSH authentication, which is `24188516-key.pem`.
- **`ubuntu@16.171.151.20`**: Connects to the instance as the `ubuntu` user, which is the default username.

After connecting, we can see system information on the console, indicating that the connection was successful.

![SSH Connection](http://127.0.0.1/assets/lab2-8.png)

### 8. List the Created Instance Using the AWS Console
The original instance created in steps 1-7 was destroyed overnight, so I had to run the commands again and the instance ID would differ. Here is a screenshot of the sucessfully created instance from the AWS console:

![AWS Console](http://127.0.0.1/assets/lab2-9.png)


## Create an EC2 Instance with Python Boto3

In this step, we create an EC2 instance using the **boto3** Python package instead of AWS CLI commands. While the method names and parameters differ, the outcome is the same as in the previous steps. To differentiate this instance from the previous one, we append `-2` to the **Group name**, **Key name**, and **Instance name**.

### Python Script
The following Python script uses `boto3` to create the EC2 **instance, security group, key pair, and instance tag**:

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
1. **`ec2.create_security_group()`**:
   - **`Description`**: Describes the purpose of the security group, here labeled as "security group for development environment".
   - **`GroupName`**: Defines the name of the security group, in this case, `24188516-sg-2`.

   This function creates a security group that will control inbound and outbound traffic for the instance.

2. **`ec2.authorize_security_group_ingress()`**:
   - **`GroupName`**: Specifies the security group where the rule will be added, in this case, `24188516-sg-2`.
   - **`IpPermissions`**: This parameter contains the rules that specify what type of inbound traffic is allowed. 
     - **`IpProtocol`**: Defines the protocol, here set to `tcp` for SSH access.
     - **`FromPort` and `ToPort`**: Both set to `22`, defining the SSH port.
     - **`IpRanges`**: Defines the IP range allowed to access the instance. Here, `0.0.0.0/0` allows access from any IP.

   This function allows SSH access to the instance by authorizing TCP traffic on port 22.

3. **`ec2.create_key_pair()`**:
   - **`KeyName`**: Specifies the name of the key pair, here `24188516-key-2`.

   This function generates a new key pair and returns the private key. The private key (`KeyMaterial`) is stored securely in a `.pem` file for later SSH access.

4. **`file.write()`**:
   - The private key is saved to a `.pem` file using Python’s built-in `open()` function, and **`os.chmod()`** is used to set the file’s permission to `400` (read-only for the owner), ensuring the file is secure and can only be read by the owner.

5. **`ec2.run_instances()`**:
   - **`ImageId`**: Specifies the Amazon Machine Image (AMI) ID, in this case, `ami-07a0715df72e58928`, which contains pre-configured software and settings.
   - **`SecurityGroupIds`**: Lists the security group IDs that will be associated with the instance. Here, the security group is `24188516-sg-2`.
   - **`MinCount` and `MaxCount`**: Define how many instances to launch. Both set to 1, indicating only one instance will be created.
   - **`InstanceType`**: Defines the type of instance to launch, in this case, `t3.micro`.
   - **`KeyName`**: Specifies the name of the key pair, `24188516-key-2`, used for SSH access.

   This function creates the EC2 instance with the specified configurations and returns the instance details, including the **InstanceId**.

6. **`ec2.create_tags()`**:
   - **`Resources`**: Specifies the resources to tag, in this case, the instance ID.
   - **`Tags`**: Defines the key-value pairs for tagging. Here, the tag key is `Name` and the value is `24188516-vm-2`, which labels the instance for easier identification.

   This function assigns the tag `24188516-vm-2` to the instance for identification purposes.

7. **`ec2.describe_instances()`**:
   - **`InstanceIds`**: Specifies the instance ID to describe.

   This function retrieves details about the instance, including the public IP address, which is necessary for SSH access.

### Output and Results
Once the script is executed, the responses from each step are printed, showing the security group creation, key pair, instance ID, and public IP address.

![Script Output](http://127.0.0.1/assets/lab2-10.png)

Let's verify the created instance in the AWS console:

![AWS Console Instance](http://127.0.0.1/assets/lab2-11.png)


## Use Docker Inside a Linux OS

### 1. Install Docker
To install Docker, we use the following command to install the necessary packages:

```bash
sudo apt install docker.io -y
```

#### Key Parameters:
- **`docker.io`**: Specifies the Docker package to install. This package includes the Docker engine and command-line tools.
- **`-y`**: Automatically confirms the installation without prompting for user input.

### 2. Start the Docker Service
After installation, we start the Docker service to make it ready for use:

```bash
sudo systemctl start docker
```

#### Key Parameters:
- **`start`**: Tells the system to start the Docker service.
- **`docker`**: Specifies the Docker service to start.

### 3. Enable Docker to Start on Boot
To ensure Docker starts automatically whenever the system boots, we enable the Docker service with:

```bash
sudo systemctl enable docker
```

#### Key Parameters:
- **`enable`**: Configures Docker to start automatically when the system boots.
- **`docker`**: Specifies the Docker service to enable.

![Docker Installation](http://127.0.0.1/assets/lab2-12.png)

### 4. Check Docker Version
To verify that Docker has been installed and is running properly, check its version using:

```bash
docker --version
```

#### Key Parameters:
- **`--version`**: Prints the installed Docker version, confirming that Docker is functional.

This command outputs the installed Docker version, ensuring that Docker is ready to use.

![Docker Version Check](http://127.0.0.1/assets/lab2-13.png)

### 5. Build and Run an `httpd` Container
In this step, we create an HTML file to be served via an Apache HTTP server running inside a Docker container.

#### HTML File Creation
The file `index.html` is located inside the `html` directory and contains the following content:

```html
  <html>
    <head></head>
    <body>
      <p>Hello, World!</p>
    </body>
  </html>
```

This file simply displays the message "Hello, World!" when accessed via a web browser.

#### Create a Dockerfile
Outside the `html` directory, we create a `Dockerfile` to define the configuration for our Docker container. The file contains the following:

```Dockerfile
FROM httpd:2.4
COPY ./html/ /usr/local/apache2/htdocs/
```

#### Key Parameters:
- **`FROM`**: Specifies the base image for the container. In this case, it uses Apache HTTP Server version 2.4.
- **`COPY`**: Copies the contents of the `html` directory from the local system into the container’s web server directory (`/usr/local/apache2/htdocs/`), making the `index.html` file accessible via the web server.

#### Add User to Docker Group
We add our username (`liudayubob`) to the Docker group to grant permission to manage Docker containers, then reboot the system:

```bash
sudo usermod -a -G docker liudayubob
```

#### Key Parameters:
- **`usermod -a -G`**: Adds the user `liudayubob` to the Docker group (`docker`), allowing them to manage Docker without using `sudo`.

#### Build the Docker Image
Once the `Dockerfile` and `html` folder are in place, we build the Docker image using the following command:

```bash
docker build -t my-apache2 .
```

#### Key Parameters:
- **`build`**: Instructs Docker to build an image based on the `Dockerfile` in the current directory.
- **`-t`**: Tags the image with the name `my-apache2` for easy reference.
- **`.`**: Specifies the build context, indicating the current directory (where the `Dockerfile` and `html` folder are located).

This command builds the Docker image, preparing it to run an Apache server that serves the `index.html` file.

![Docker Build](http://127.0.0.1/assets/lab2-14.png)


#### Run the Docker Container
After building the image `my-apache2`, we run the Docker container using the following command:

```bash
docker run -p 80:80 -dit --name my-app my-apache2
```

#### Key Parameters:
- **`-p`**: Maps the host machine's port to the Docker container's port, enabling access to the container’s web server from the host.
- **`-dit`**: Runs the container in detached mode (`d`), keeps STDIN open (`i`), and allocates a pseudo-TTY (`t`).
- **`--name`**: Sets the container name to `my-app`.

This command starts the Apache server inside the container, serving the HTML content at port 80.

![Docker Run](http://127.0.0.1/assets/lab2-15.png)

#### Access the Hosted HTML Page
To view the hosted HTML page, open a browser and navigate to `http://localhost` or `http://127.0.0.1`. The browser will display the "Hello, World!" message from the `index.html` file served by the Apache HTTP server inside the Docker container.

![Docker Webpage](http://127.0.0.1/assets/lab2-16.png)


### 6. Other Docker Commands

#### Check Running Containers
To list all running containers, use the following command:

```bash
docker ps -a
```

#### Key Parameters:
- **`ps`**: Lists the currently running containers.
- **`-a`**: Includes all containers, even those that are not running.

This command displays the properties of the containers, such as **Container ID**, **STATUS**, **PORTS**, the container name, and the image used.

![Docker ps -a](http://127.0.0.1/assets/lab2-17.png)

#### Stop and Remove the Container
To stop and remove the running container, use the following commands:
```bash
docker stop my-app
docker rm my-app
```

#### Key Parameters:
- **`stop`**: Stops the running container.
- **`rm`**: Removes the container from the system.

These commands stop the `my-app` container and then remove it from the system.


<div  style="page-break-after: always;"></div>


# Lab 3

### 1. Preparation
We begin by creating the required files and directories. The following file structure contains three files: `cloudstorage.py`, `rootfile.txt`, and `subfile.txt`.

![File Structure](http://127.0.0.1/assets/lab2-18.png)


### 2. Save to S3 by Updating `cloudstorage.py`
The `cloudstorage.py` script is modified to create an S3 bucket named `24188516-cloudstorage` if it doesn’t already exist. The script then traverses all directories and subdirectories in the root directory and uploads any discovered files to the S3 bucket.

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

### Code Explanation

- **`s3.create_bucket()`**: Attempts to create an S3 bucket.
  - **`Bucket`**: Specifies the name of the bucket to be created, which is `24188516-cloudstorage`.
  - **`CreateBucketConfiguration`**: Defines configuration options for the bucket. In this case, we set the `LocationConstraint` to `eu-north-1`, which places the bucket in the specified AWS region.
 
- **`os.walk()`**: Recursively traverses through the root directory (`.`) and subdirectories, finding all files to be uploaded.

- **`s3.upload_file()`**: Uploads the file to the S3 bucket. It accepts the following parameters:
  - **`file`**: The local path to the file to upload.
  - **`Bucket`**: Specifies the destination S3 bucket, `24188516-cloudstorage`.
  - **`file_name`**: The key under which the file is stored in the S3 bucket, formed by concatenating the folder path and file name.

The method **`s3.upload_file()`** ensures the file is uploaded to the correct location in S3, maintaining the local directory structure.

![S3 Upload](http://localhost/assets/lab2-19.png)



### 3. Restore from S3
We create a new program, `restorefromcloud.py`, to restore files from the S3 bucket and write them to the appropriate directories. The program uses `s3.list_objects_v2` to list all files in the S3 bucket along with their attributes, such as **Key** and **Name**.

We combine the local **ROOT_TARGET_DIR** with the **Key** to form the local file path. If the local directory does not exist, we create it using `os.makedirs()`. Finally, we download each file from the S3 bucket using `s3.download_file()`.

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

### Code Explanation

- **`boto3.client("s3")`**: Initializes the S3 client for interacting with the S3 bucket.
  
- **`s3.list_objects_v2()`**: Lists all objects stored in the specified S3 bucket.
  - **`Bucket`**: Specifies the S3 bucket name, here `24188516-cloudstorage`, from which we are retrieving files.

- **`s3.download_file()`**: Downloads the specified file from S3 to the local directory.
  - **`Bucket`**: Specifies the S3 bucket name, `24188516-cloudstorage`.
  - **`s3_key`**: The key (path) of the file in the S3 bucket.
  - **`local_file_path`**: Specifies the destination file path on the local machine.

- **`os.makedirs()`**: Creates the specified directory if it doesn’t already exist, ensuring the local directory structure mirrors the S3 directory structure.

This script traverses the S3 bucket, restoring files to the local directory in the same structure they were uploaded.

![S3 Restore](http://localhost/assets/lab2-20.png)

### 4. Write Information About Files to DynamoDB

#### 1. Install DynamoDB
First, we create and navigate into the `dynamodb` directory. We then install **JRE** and download the **DynamoDB** package, extracting the necessary files for local use. Once extracted, we have the compiled Java code `DynamoDBLocal.jar` and a folder containing libraries `DynamoDBLocal_lib`, which are required to run a local DynamoDB instance.

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

Next, we start the DynamoDB instance locally using **JRE**. The port is set to **8001** since **8000** is already in use. The `-sharedDb` flag creates a single database file, `_shared-local-instance.db`, which is accessed by all programs connecting to this local DynamoDB instance.

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar –sharedDb -port 8001
```

#### Key Parameters:
- **`-Djava.library.path`**: Specifies the path to the required native libraries for running DynamoDB locally, which is `./DynamoDBLocal_lib`.
- **`-jar`**: Indicates the JAR file `DynamoDBLocal.jar` that contains the DynamoDB local service.
- **`-sharedDb`**: Configures DynamoDB to use a single shared database file (`_shared-local-instance.db`).
- **`-port`**: Specifies that the service should listen on port 8001.

![Start DynamoDB](http://localhost/assets/lab2-22.png)


#### 2. Create a Table in DynamoDB
We create a Python script, `createtable.py`, to define a table named `CloudFiles` in DynamoDB. The table uses `userId` as the partition key and `fileName` as the sort key. We define the keys using `KeyType` (`HASH` for partition key and `RANGE` for sort key), while `AttributeName` and `AttributeType` specify the attributes' names and types.

Although DynamoDB is schema-free, attributes like `path`, `lastUpdated`, `owner`, and `permissions` don’t need to be predefined in the table schema, but they can be added later when inserting items into the table.

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

### Code Explanation

- **`boto3.resource("dynamodb")`**: Initializes a DynamoDB resource instance, allowing interaction with the DynamoDB service. We specify `endpoint_url="http://localhost:8001"` to connect to the local DynamoDB instance running on port **8001**.
  
- **`dynamodb.create_table()`**: Creates a new table in DynamoDB.
  - **`TableName`**: Specifies the name of the table, here `CloudFiles`.
  - **`KeySchema`**: Defines the partition key and sort key for the table:
    - **`AttributeName`**: Specifies the name of the attribute. We use `userId` for the partition key and `fileName` for the sort key.
    - **`KeyType`**: Specifies whether the attribute is a partition key (`HASH`) or a sort key (`RANGE`).
  - **`AttributeDefinitions`**: Specifies the types of attributes used in the key schema:
    - **`AttributeType`**: Defines the type of the attribute. In this case, both `userId` and `fileName` are of type `S` (string).
  - **`ProvisionedThroughput`**: Defines the read and write capacity for the table. Here, both read and write capacity are set to 1.

The script connects to the local DynamoDB instance, creates the `CloudFiles` table, and prints the table status after creation.

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

### Code Explanation

- **`s3.list_objects_v2()`**: Lists all objects in the specified S3 bucket.
  - **`Bucket`**: Specifies the name of the bucket to retrieve the object list from, in this case, `24188516-cloudstorage`.
  
- **`s3.get_object_acl()`**: Retrieves the access control list (ACL) of the specified object to get details like the owner and permissions.
  - **`Bucket`**: Specifies the S3 bucket name, `24188516-cloudstorage`.
  - **`Key`**: Specifies the key (path) of the object for which the ACL is retrieved.

- **`dynamodb_table.put_item()`**: Inserts an item into the DynamoDB table.
  - **`Item`**: Specifies the attributes of the item to insert. In this case, it includes attributes like `userId`, `fileName`, `path`, `lastUpdated`, `owner`, and `permissions`.

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

#### Key Parameters:
- **`--table-name`**: Specifies the name of the DynamoDB table to scan, in this case, `CloudFiles`.
- **`--endpoint-url`**: Specifies the endpoint URL for connecting to the local DynamoDB instance running on port **8001**.

This command prints the table structure, showing the data we inserted in the previous step.

![DynamoDB Scan](http://localhost/assets/lab2-25.png)

#### Destroy the Table
To delete the `CloudFiles` table, we use the following AWS CLI command:

```bash
aws dynamodb delete-table --table-name CloudFiles --endpoint-url http://localhost:8001
```

#### Key Parameters:
- **`--table-name`**: Specifies the name of the DynamoDB table to delete, in this case, `CloudFiles`.
- **`--endpoint-url`**: Specifies the endpoint URL for connecting to the local DynamoDB instance running on port **8001**.

This command deletes the table, removing all data and schema. Only the defined schema (partition key and sort key) will be printed before deletion.

![DynamoDB Delete Table](http://localhost/assets/lab2-26.png)

<div  style="page-break-after: always;"></div>


# Lab 4
## Apply a Policy to Restrict Permissions on Bucket

### 1. Write a Python Script
In this lab, we apply an access permission policy to the S3 bucket `24188516-cloudstorage` created in the previous lab. The policy restricts access to this bucket, allowing only the user with the username `24188516@student.uwa.edu.au` to access the contents. 

The policy is defined as a JSON document, where:
- **`Sid`**: A unique identifier for the policy statement.
- **`Effect`**: Specifies the result of the policy, set to `"DENY"`, meaning the action is denied if the condition is met.
- **`Action`**: Specifies the S3 actions being denied, in this case, `"s3:*"` to deny all S3 actions.
- **`Resource`**: Specifies the resources affected by the policy, here all objects in the `24188516-cloudstorage` bucket.
- **`Condition`**: Specifies a condition that checks if the `aws:username` is not `24188516@student.uwa.edu.au`. If true, access is denied.

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

This JSON policy ensures that any user attempting to access the bucket, who is not `24188516@student.uwa.edu.au`, will be denied all actions related to S3. The policy applies to all objects within the `24188516-cloudstorage` bucket, as specified by the **`Resource`**.

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

### Code Explanation
- **`boto3.client('s3')`**: Initializes an S3 client for interacting with the S3 service.
  
- **`json.load()`**: Reads and parses the `bucketpolicy.json` file into a Python dictionary.

- **`json.dumps()`**: Converts the Python dictionary containing the policy into a JSON string format, which is required by the `put_bucket_policy()` method.

- **`s3.put_bucket_policy()`**: Applies the bucket policy to the specified S3 bucket.
  - **`Bucket`**: Specifies the name of the S3 bucket, here `24188516-cloudstorage`.
  - **`Policy`**: Accepts the policy as a JSON string, which defines the access control rules for the bucket.

This script does the following:
1. Reads the JSON policy from `bucketpolicy.json`.
2. Converts the policy into a string format.
3. Applies the policy to the S3 bucket using `s3.put_bucket_policy()`.

![Applying S3 Bucket Policy](http://localhost/assets/lab4-1.png)

### 2. Check Whether the Script Works
After applying the bucket policy, we test to ensure that the policy is working as intended.

#### Verify the Policy Using AWS CLI
To check whether the policy has been applied to the `24188516-cloudstorage` bucket, we use the following AWS CLI command:

```bash
aws s3api get-bucket-policy --bucket 24188516-cloudstorage --query Policy --output text
```

#### Key Parameters:
- **`--bucket`**: Specifies the name of the S3 bucket to check for the applied policy, in this case, `24188516-cloudstorage`.
- **`--query Policy`**: Filters the output to display only the bucket policy.
- **`--output text`**: Outputs the policy in plain text format.

This command retrieves the policy attached to the S3 bucket and outputs it in plain text. The expected output is the JSON policy document we applied earlier.

![Policy Check with AWS CLI](http://localhost/assets/lab4-2.png)


#### Visual Confirmation via AWS Console
Next, we navigate to the AWS console to visually confirm that the policy is in place for the `24188516-cloudstorage` bucket. The console should display the same policy, with the conditions we set for restricting access based on the username.

![Policy Check in AWS Console](http://localhost/assets/lab4-3.png)

#### Test Denied Access with Incorrect Username
To test whether the policy is correctly restricting access, we deliberately alter the username in the policy. For example, we change the username condition to only allow access to `12345678@student.uwa.edu.au`, effectively denying access to the current user `24188516@student.uwa.edu.au`.

![Denied Access](http://localhost/assets/lab4-4.png)
![Access Denied](http://localhost/assets/lab4-5.png)

As expected, when trying to access the bucket resources under the user `24188516@student.uwa.edu.au`, the access is denied.

## AES Encryption Using KMS

### 1. Policy to be Attached to the KMS Key

The following JSON file, `kmspolicy.json`, defines the access control policy to be attached to the KMS (Key Management Service) key. This policy grants permissions to both the root account and the IAM user (`24188516@student.uwa.edu.au`), ensuring appropriate access levels for key management and cryptographic operations.

#### Breakdown of the Policy:
- **Version**: `"2012-10-17"` – This version of the policy language is required for policy documents.
- **Statements**: The policy contains four main statements:
  1. **Root Account Permissions**: Grants the root account full access to KMS operations.
  2. **Key Administrators**: Grants the IAM user permissions for key management tasks.
  3. **Use of the Key**: Grants the IAM user permissions for encryption, decryption, and other cryptographic operations.
  4. **Grant Management**: Allows the IAM user to manage grants, ensuring the grants are for AWS resources.
 
Here’s the full JSON policy:

```json
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

#### Key Aspects of the Policy:
- **Root Account Permissions**: Grants full access (`kms:*`) to the root account (`arn:aws:iam::489389878001:root`) for all KMS operations on all resources.
- **Key Management for IAM User**: The IAM user (`24188516@student.uwa.edu.au`) is granted permissions to perform key management tasks such as **creating, describing, enabling, disabling, tagging, and deleting keys**.
- **Cryptographic Operations**: The IAM user can use the key for cryptographic functions like **encrypting, decrypting, re-encrypting, and generating data keys**.
- **Grant Management**: Allows the IAM user to manage grants (e.g., **creating, listing, and revoking** grants) for the key, but only when the grant is for an AWS resource (`kms:GrantIsForAWSResource`).

This policy ensures secure management of the KMS key, allowing only authorized users to perform key management and cryptographic operations.


### 2. Attach a Policy to the Created KMS Key

In this step, we create a symmetric encryption KMS key and apply the policy from the `kmspolicy.json` file that was defined earlier. The KMS key is specified for encryption and decryption purposes. After the key is created, we assign an alias using the student's ID, following the format `alias/*`, which results in `alias/24188516`.

Here’s the Python script that performs these operations:

```python
import boto3
import json

STUDENT_NUMBER = '24188516'

def create_kms_key():
    # Import the policy from the JSON file
    with open('kmspolicy.json', 'r') as policy_file:
        policy = json.load(policy_file)

    # Create a new KMS key with the imported policy
    kms = boto3.client('kms')
    key_response = kms.create_key(
        Policy=json.dumps(policy),
        KeyUsage='ENCRYPT_DECRYPT',
        Origin='AWS_KMS'
    )
    
    # Extract the KeyId from the response
    key_id = key_response['KeyMetadata']['KeyId']

    # Create an alias for the KMS key using the student number
    alias_name = f'alias/{STUDENT_NUMBER}'
    alias_response = kms.create_alias(
        AliasName=alias_name,
        TargetKeyId=key_id
    )
    
    print(f"Key and alias generated successfully!")

if __name__ == "__main__":
    create_kms_key()
```

#### Explanation of the Script:
1. **Policy Import**: The `kmspolicy.json` file is loaded using `json.load()` and converted into a string using `json.dumps()`. This policy defines the permissions for both the root account and the IAM user (`24188516@student.uwa.edu.au`).
2. **Create KMS Key**: A new KMS key is created using `kms.create_key()`. The key is specified for encryption and decryption with the `KeyUsage='ENCRYPT_DECRYPT'` parameter.
3. **Key ID**: The response from the `create_key()` call contains metadata, including the `KeyId`, which we extract for further use.
4. **Create Alias**: The `kms.create_alias()` function creates an alias for the newly generated KMS key. The alias follows the format `alias/24188516` where `24188516` is the student's ID.

#### Output:
Once the script is executed, a symmetric KMS key is created with the policy applied, and an alias (`alias/24188516`) is assigned to the key.

![KMS Key and Alias](http://localhost/assets/lab4-6.png)

### Key Points:
- **KMS Key Creation**: The key is created specifically for encryption and decryption operations.
- **Alias Assignment**: The alias `alias/24188516` provides a human-readable reference to the key, simplifying future key management.

### 3. Check Whether the Script Works

To verify that the script has successfully created the KMS key and applied the policy, follow these steps:

#### 1. Check the KMS Key in the AWS Console
Navigate to the **KMS service** in the AWS console. In the list of keys, you should see the newly created key with the alias `alias/24188516`. This confirms that the KMS key and alias have been successfully generated.

![KMS Key and Alias](http://localhost/assets/lab4-7.png)

#### 2. Verify the Policy
In the **Policy** section of the KMS key, you should see that the user `24188516@student.uwa.edu.au` has been assigned the roles of **Key Administrator** and **Key User**. This confirms that the policy from the `kmspolicy.json` file has been correctly applied to the key, granting the appropriate permissions to the IAM user.

![Policy Verification](http://localhost/assets/lab4-8.png)

### Key Points:
- **KMS Key Creation**: The key is successfully created with the alias `alias/24188516`.
- **Policy Application**: The IAM user `24188516@student.uwa.edu.au` is assigned as both the **Key Administrator** and **Key User**, confirming the policy has been applied correctly.

### 4. Use the Created KMS Key for Encryption/Decryption

The following script, `cryptwithkms.py`, encrypts and decrypts files in the S3 bucket `24188516-cloudstorage` using the KMS key we created earlier (`alias/24188516`).

#### Workflow:
1. The script first lists all files in the specified S3 bucket.
2. For each file, the **`encrypt_file()`** function retrieves the file content from S3, encrypts it using the specified KMS key, and uploads the encrypted file back to the bucket with a new key that appends `.encrypted` to the original file name.
3. After encrypting the file, it calls the **`decrypt_file()`** function to decrypt the file content and uploads the decrypted file back to the bucket with a new key that appends `.decrypted` to the encrypted file name.

Here’s the Python script:

```python
# cryptwithkms.py
import boto3

s3 = boto3.client('s3')
kms = boto3.client('kms')

BUCKET_NAME = "24188516-cloudstorage"
KMS_KEY = "alias/24188516"

def encrypt_file(file_key):
    # Get the file from bucket and read its content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = s3_object['Body'].read()

    # Encrypt the file content using KMS
    encrypt_res = kms.encrypt(
        KeyId=KMS_KEY,
        Plaintext=file_content
    )
    file_body = encrypt_res['CiphertextBlob']
    encrypt_file_key = f"{file_key}.encrypted"

    # Upload the encrypted file back to the bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=encrypt_file_key, Body=file_body)
    print(f"File encrypted as: {encrypt_file_key} with content: \n{file_body}\n")
    
    # After encrypting, decrypt the file
    decrypt_file(encrypt_file_key)

def decrypt_file(file_key):
    # Get the encrypted file from the bucket and read its content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = s3_object['Body'].read()

    # Decrypt the file content using KMS
    decrypt_res = kms.decrypt(
        KeyId=KMS_KEY,
        CiphertextBlob=file_content
    )
    plain_text = decrypt_res['Plaintext']
    file_body = plain_text.decode('utf-8')  # Convert plain text bytes to a regular string
    decrypted_file_key = f"{file_key}.decrypted"

    # Upload the decrypted content back to the bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_file_key, Body=file_body)
    print(f"File decrypted as: {decrypted_file_key} with content: \n{file_body}\n")

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

#### Explanation of the Script:
1. **`encrypt_file(file_key)`**:
   - Retrieves the file from the S3 bucket using `s3.get_object()`.
   - Encrypts the file content using the KMS key with `kms.encrypt()`.
   - Uploads the encrypted content back to the bucket with a new key that appends `.encrypted` to the original file name.
   - Calls `decrypt_file()` to decrypt the encrypted file.

2. **`decrypt_file(file_key)`**:
   - Retrieves the encrypted file from the bucket using `s3.get_object()`.
   - Decrypts the file content using the KMS key with `kms.decrypt()`.
   - Converts the decrypted content from bytes to a regular string using `.decode('utf-8')`.
   - Uploads the decrypted content back to the bucket with a new key that appends `.decrypted` to the encrypted file name.

3. **`process_files(BUCKET_NAME, KMS_KEY)`**:
   - Lists all files in the specified S3 bucket.
   - Iterates through each file, calling `encrypt_file()` for encryption and subsequent decryption.

![Encryption/Decryption Process](http://localhost/assets/lab4-9.png)

#### Verify Results in the AWS S3 Console
After running the script, you can verify the encrypted and decrypted files in the AWS S3 console. The original files will have additional encrypted and decrypted versions as shown below.

![S3 Encrypted Files](http://localhost/assets/lab4-10.png)
![S3 Decrypted Files](http://localhost/assets/lab4-11.png)

### Key Points:
- **Encryption/Decryption**: The script successfully encrypts files using KMS and decrypts them, both operations being performed on files stored in the S3 bucket.
- **File Naming**: The encrypted and decrypted files are stored with `.encrypted` and `.decrypted` appended to their original names, making it easy to track each file's status.

### 5. Apply `pycryptodome` for Encryption/Decryption

Since AWS KMS uses AES with 256-bit encryption, we can apply the same encryption standard using the `pycryptodome` package for consistency. Here's how we implement AES encryption and decryption with `pycryptodome`.

#### 1. Install `pycryptodome`
First, install the `pycryptodome` package by running the following command:

```bash
pip install pycryptodome
```

This package provides AES encryption functionality similar to what AWS KMS offers.

![Pycryptodome Installation](http://localhost/assets/lab4-12.png)

#### 2. Modify the Code in `cryptwithpycryptodome.py`
The code is similar to the `cryptwithkms.py` script from the previous step, but now we use `pycryptodome` for encryption and decryption.

##### Key Differences:
- **Import AES and Random Byte Generation**: We import `AES` from `pycryptodome` for encryption/decryption and `get_random_bytes` for random key generation. The **AES_KEY** is **32 bytes** (256 bits) long, aligning with the AWS KMS approach.

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

AES_KEY = get_random_bytes(32)  # 32 bytes = 256 bits-long key
```

- **Encryption Process**:
  - We initialize an AES cipher object in EAX mode with the generated `AES_KEY`: `AES.new(AES_KEY, AES.MODE_EAX)`.
  - The file content is encrypted using `cipher.encrypt_and_digest()`, which generates the ciphertext and an authentication tag for integrity verification.
  - We concatenate the **nonce**, **tag**, and **ciphertext** in that order to create the encrypted file content. The nonce is used to ensure unique ciphertexts for the same plaintext, preventing issues like hash collisions.

```python
# Encrypt the file content using AES with PyCryptodome in EAX mode
cipher = AES.new(AES_KEY, AES.MODE_EAX)
cipher_text, tag = cipher.encrypt_and_digest(file_content)  # Encrypt and generate tag
encrypt_file_key = f"{file_key}.encrypted"

# Concatenate the nonce, tag, and the ciphertext
file_body = cipher.nonce + tag + cipher_text
```

- **Decryption Process**:
  - We extract the **nonce**, **tag**, and **ciphertext** from the concatenated file content (`file_body`). The nonce is the first 16 bytes, the tag is the next 16 bytes, and the remaining content is the ciphertext.
  - Using the extracted nonce, we create a new AES cipher object to decrypt the file and verify its integrity with the tag.

```python
# Parse the nonce, tag, and the ciphertext from the file content
nonce = file_body[:16]  # First 16 bytes for the nonce
tag = file_body[16:32]  # Next 16 bytes for the tag
cipher_text = file_body[32:]  # The remaining bytes are the ciphertext

# Decrypt the file content using AES with PyCryptodome in EAX mode
cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
plain_text = cipher.decrypt_and_verify(cipher_text, tag)
file_body = plain_text.decode('utf-8')  # Convert decrypted content to a string
```

Here’s the full modified script:

```python
# cryptwithpycryptodome.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "24188516-cloudstorage"
AES_KEY = get_random_bytes(32)  # 256-bit key

def encrypt_file(file_key):
    # Get the file from the bucket and read content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = s3_object['Body'].read()

    # Encrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(file_content)
    encrypt_file_key = f"{file_key}.encrypted"

    # Concatenate the nonce, tag, and ciphertext
    file_body = cipher.nonce + tag + cipher_text

    # Upload the encrypted file back to the bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=encrypt_file_key, Body=file_body)
    print(f"File encrypted as: {encrypt_file_key} with content: \n{file_body}\n")
    
    # Decrypt the file after encryption
    decrypt_file(encrypt_file_key)

def decrypt_file(file_key):
    # Get the encrypted file from the bucket and read content
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_body = s3_object['Body'].read()

    # Parse the nonce, tag, and ciphertext from the file content
    nonce = file_body[:16]  # First 16 bytes for the nonce
    tag = file_body[16:32]  # Next 16 bytes for the tag
    cipher_text = file_body[32:]  # The rest of the file content is the ciphertext

    # Decrypt the file content using AES with PyCryptodome in EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    plain_text = cipher.decrypt_and_verify(cipher_text, tag)
    file_body = plain_text.decode('utf-8')  # Convert plain text bytes to a regular string
    decrypted_file_key = f"{file_key}.decrypted"

    # Upload the decrypted content back to the bucket
    s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_file_key, Body=file_body)
    print(f"File decrypted as: {decrypted_file_key} with content: \n{file_body}\n")

def process_files(BUCKET_NAME):
    # List all files in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            encrypt_file(key)

if __name__ == "__main__":
    process_files(BUCKET_NAME)
```

#### 3. See It in Action
Now, let's run the script using:

```bash
python3 cryptwithpycryptodome.py
```

The encrypted content will differ from the previous method since a different encryption key is used.

![Encrypted Content](http://localhost/assets/lab4-13.png)

You can verify the encrypted and decrypted files in the AWS S3 console:

![S3 Encrypted Files](http://localhost/assets/lab4-10.png)
![S3 Decrypted Files](http://localhost/assets/lab4-11.png)

### Key Points:
- **Encryption Consistency**: We use AES with a 256-bit key, ensuring consistency with the AWS KMS approach.
- **Encryption/Decryption Process**: The script uses PyCryptodome's AES encryption in EAX mode to secure the files, similar to how KMS operates.
- **File Handling**: Encrypted and decrypted files are stored in the S3 bucket with `.encrypted` and `.decrypted` appended to their original names.

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

### 1-2. Create 2 EC2 Instances & Add Application Load Balancer

In this section, we will replicate some of the steps from **Lab 2** to create two EC2 instances, but with a few changes to accommodate the new resources for **Lab 5**. We append the suffix `lab5` to resource names like **security group** and **key pair** to differentiate them from the resources in **Lab 2**.

#### Key Changes:
- **Subnets and Availability Zones**: We will create the two EC2 instances in different **availability zones** by using `ec2.describe_subnets()` to fetch the subnets, and specifying the **SubnetId** parameter when launching the EC2 instances.
- **Load Balancer and Target Group**: 
  - **Create Load Balancer**: Using `elbv2.create_load_balancer()` with the required subnets, security groups, and settings.
  - **Create Target Group**: Using `elbv2.create_target_group()` with the VPC ID, protocol, and port.
  - **Register Targets**: Register the EC2 instances to the load balancer target group.
  - **Create Listener**: Set up a listener to forward HTTP traffic from **port 80** to the **target group**.

#### Python Script for Automation:

```python
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
# Save key-pair
with open(f'{KeyName}.pem', 'w') as file:
    file.write(PrivateKey)
# Grant file permission
os.chmod(f'{KeyName}.pem', 0o400)

# 4. Get two subnets in different availability zones
step4_response = ec2.describe_subnets()['Subnets']
Subnets = [subnet['SubnetId'] for subnet in step4_response[:2]]

# 5. Create instances in two availability zones
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
    
    # Tag instance with name
    ec2.create_tags(
        Resources=[InstanceId],
        Tags=[{'Key': 'Name', 'Value': InstanceName}]
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

# Print results
print(f"Instance IDs: {Instances}")
print(f"Load Balancer ARN: {LoadBalancerArn}")
print(f"Target Group ARN: {TargetGroupArn}")
```

#### Steps Summary:
1. **Security Group**: Creates a security group for **SSH (port 22)** and **HTTP (port 80)** access.
2. **Key Pair**: Generates a key pair for accessing the instances.
3. **Subnet Selection**: Fetches two subnets from different availability zones using `ec2.describe_subnets()`.
4. **Create EC2 Instances**: Launches two EC2 instances in separate availability zones, and assigns names to each instance.
5. **Load Balancer**: Creates an application load balancer that is internet-facing and linked to the security group and subnets.
6. **Target Group**: Creates a target group for the EC2 instances, specifying the VPC and HTTP port 80.
7. **Register Instances**: Registers the EC2 instances as targets for the load balancer.
8. **Listener**: Sets up a listener to forward traffic from **port 80** to the target group.

#### Verify in the AWS Console:
After the script is executed, you can verify the creation of the **load balancer** and **target group** in the AWS console.

![Load Balancer Created](http://localhost/assets/lab5-2.png)
![Target Group Created](http://localhost/assets/lab5-3.png)

#### Record Public IP Addresses:
The public IPv4 addresses for both EC2 instances are recorded for verification.

![EC2 Public IPs](http://localhost/assets/lab5-4.png)

### 3. SSH to Our Instances

In this step, we will SSH into the EC2 instances to install Apache and start the web server, allowing us to see the load balancer in action.

#### Use Putty to Connect to EC2 Instances
Since we are using Windows and Putty as our SSH client, we need to convert the private key (`24188516-key-lab5.pem`) to **PPK format** for Putty to use.

#### 1. Convert PEM Key to PPK Format
1. Open **PuttyGen** and load the `.pem` key file that was generated in step [3].
2. Convert the file into `.ppk` format by saving it after loading.

![PuttyGen Conversion](http://localhost/assets/lab5-5.png)

#### 2. Configure Putty for SSH Access
Once the key is converted, we can configure Putty to use the correct authentication credentials and the public IP addresses of the two EC2 instances we recorded in the last step.

1. **Host**: Enter the public IP address of the EC2 instance you want to connect to.
2. **Authentication**: Under "Connection -> SSH -> Auth", browse and load the `.ppk` file for the private key.

![Putty Configuration](http://localhost/assets/lab5-6.png)
![Putty Host Setup](http://localhost/assets/lab5-7.png)

#### 3. SSH into the EC2 Instance
Now, click "Open" to initiate the SSH connection. You will be logged into the EC2 instance.

![SSH Connection Established](http://localhost/assets/lab5-8.png)

### Key Points:
- **Key Conversion**: We use PuttyGen to convert the `.pem` key into `.ppk` format for use in Putty.
- **Putty Configuration**: The correct IP address and key are configured in Putty to establish the SSH connection.
- **Successful Login**: After configuration, we can successfully SSH into both EC2 instances.

### 4. Install Apache & Access Results Using IP Addresses

In this step, we will install **Apache** on each EC2 instance, modify the HTML content, and verify the setup by accessing the instances via their public IP addresses.

#### 1. Update and Install Apache
On each EC2 instance, first update the package list and then install **Apache2** using the following commands:

```bash
sudo apt-get update
sudo apt install apache2
```

Once the installation is complete, Apache will start serving content from the default directory `/var/www/html/`.

![Apache Installation](http://localhost/assets/lab5-9.png)

#### 2. Modify the HTML File to Display Instance Name
To help us identify which EC2 instance is serving the content, we will edit the `<title>` tag of the default `index.html` file to include the instance name. Use the following command to edit the file:

```bash
sudo vi /var/www/html/index.html
```

Here’s an example of the modified HTML file for **VM1**:

```html
# index.html
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Hello, this is VM1!</title>
<style type="text/css" media="screen">
```

You can repeat this step for the second instance (VM2) and modify the `<title>` tag accordingly.

![HTML Modification](http://localhost/assets/lab5-10.png)

#### 3. Access the EC2 Instances via Public IP Addresses
Now that Apache is running and the HTML content has been updated, we can access each instance using its public IP address. Open your browser and visit the public IP addresses assigned to each instance.

- **VM1** will display the title: "Hello, this is VM1!"
  
![VM1 Display](http://localhost/assets/lab5-11.png)

- **VM2** will display the title: "Hello, this is VM2!"

![VM2 Display](http://localhost/assets/lab5-12.png)

### Key Points:
- **Apache Installation**: Apache is installed on each instance, allowing us to serve content from `/var/www/html/`.
- **HTML Modification**: The title of the HTML page is updated to reflect the instance name, making it easy to distinguish between the two EC2 instances.
- **Access via IP**: The public IP addresses are used to access each instance and verify that the HTML modifications are displayed.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExNjQ1NTY0MjEsLTYyNDM0Mzg3Nyw3Mz
UyMDY5MjksLTEwMjQyMDU0NCwtMTQyMjM0NzE4MCwzNzM4OTQz
NTAsLTIwNTAwMTIxMzIsLTk0ODE4NzQsNTYwODU5NDE2LDE0Mz
YzODQzNjYsLTkxMTY0MDYyMCwtMjA4ODc0NjYxMl19 
-->
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg0NzQ0NTQ1MCwtMTc4NTEwMDgyLDUxNz
g2ODM0MCwtMjIzNTIwMjk3LC03NzcyNzUwNTksNTM1MjM5NDMy
LDUzMzE3MzM4Niw0MzA3NTcxNDksLTEzMjI0MTI0NDksMzk5Nj
Y1NjkyLC0xMTg3MDcxODA5LDE0ODM1MjY0MjMsOTQ1NzI3NjQx
LDE1MzMwNDg1NDMsNTQxNzQ4NDQ0LDEzNDcxMzEwMDgsMTIxND
k4Nzc3MSwtMTU0OTg3MTM5NSwtMTI1MTM2MTQyNywtOTI4Mzkz
OTcxXX0=
-->