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

#### (1) install dependencies
The pandas library is used here to convert un-tabulated data into structured table.
Run the following code to install the extra dependency
`pip install pandas`

#### (2) explain the code
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

#### (3) run the script

run the following code to execute the python script:
`python3 lab1.py`

#### [4] get the results
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
describe-instances returns available information to the instance with `--instance-ids`, since we only want the IP address for ssh purpose, the query limits the output to only `Reservations[0].Instances[0].PublicIpAddress`
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
The original instance was destoyed over night so you might see the instance id has changed

## Create an EC2 instance with Python Boto3

Use a Python script to implement the steps above (steps 1-6 and 8 are required, step 7 is optional). Refer to [page](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html) for details.

**NOTE**: When you are done, log into the EC2 console and terminate the instances you created.

## Use Docker inside a Linux OS

### [1] Install Docker
```
sudo apt install docker.io -y
```

### [2] Start Docker
```
sudo systemctl start docker
```

### [3] Enable Docker
```
sudo systemctl enable docker
```

### [4] Check the version

```
docker --version
```

### [5] Build and run an httpd container

Create a directory called html

Edit a file index.html inside the html directory and add the following content

```
  <html>
    <head> </head>
    <body>
      <p>Hello World!</p>
    </body>
  </html>
```

Create a file called Dockerfile outside the html directory with the following content:

```
FROM httpd:2.4
COPY ./html/ /usr/local/apache2/htdocs/
```

Build a docker image

```
docker build -t my-apache2 .
```

If you run into permission errors, you may need add your user to the docker group:

```
sudo usermod -a -G docker <username>
```

Be sure to log out and log back in for this change to take effect.

Run the image

```
docker run -p 80:80 -dit --name my-app my-apache2
```

Open a browser and access address: http://localhost or http://127.0.0.1. 

Confirm you get "Hello World!"

### [6] Other docker commands

To check what is running

```
docker ps -a
```
To stop and remove the container

```
docker stop my-app
docker rm my-app
```

<div  style="page-break-after: always;"></div>

# Lab 3

<div  style="page-break-after: always;"></div>

# Lab 4

<div  style="page-break-after: always;"></div>

# Lab 5
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1OTg3Njc0OTUsLTk0ODE4NzQsNTYwOD
U5NDE2LDE0MzYzODQzNjYsLTkxMTY0MDYyMCwtMjA4ODc0NjYx
Ml19
-->