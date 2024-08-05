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

```
aws ec2 create-security-group --group-name <student number>-sg --description "security group for development environment"
```

This will use the default VPC (if you want to specify a VPC, use --vpc-id vpc-xxxxxxxx). Take a note of the security group id that is created. 

### [2] Authorise inbound traffic for ssh

```
aws ec2 authorize-security-group-ingress --group-name <student number>-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
```

### [3] Create a key pair

```
aws ec2 create-key-pair --key-name <student number>-key --query 'KeyMaterial' --output text > <student number>-key.pem
```

To use this key on Linux, copy the file to a directory ~/.ssh and change the permissions to:

```
chmod 400 <student number>-key.pem
```
### [4] Create the instance 

| Student Number | Region | Region Name | ami id |
| --- | --- | --- | --- |
| 20666666 – 22980000 | US East (N. Virginia) |	us-east-1 |	ami-0a0e5d9c7acc336f1 |
| 22984000 – 23370000 | Asia Pacific (Tokyo)	| ap-northeast-1	| ami-0162fe8bfebb6ea16 |
| 23400000 – 23798000 | Asia Pacific (Seoul)	| ap-northeast-2	| ami-056a29f2eddc40520 |
| 23799000 – 23863700 | Asia Pacific (Osaka)	| ap-northeast-3	| ami-0a70c5266db4a6202 |
| 23864000 – 23902200 | Asia Pacific (Mumbai)	| ap-south-1	| ami-0c2af51e265bd5e0e |
| 23904000 – 23946000 | Asia Pacific (Singapore)	| ap-southeast-1	| ami-0497a974f8d5dcef8 |
| 23946100 – 24024000 | Asia Pacific (Sydney)	| ap-southeast-2	| ami-0375ab65ee943a2a6 |
| 24025000 – 24071000 | Canada (Central)	| ca-central-1	| ami-048ddca51ab3229ab |
| 24071100 – 24141000 | Europe (Frankfurt)	| eu-central-1	| ami-07652eda1fbad7432 |
| 24143000 – 24700000 | Europe (Stockholm)	| eu-north-1	| ami-07a0715df72e58928 |


Based on your region code, find the corresponding ami id in the table above and fill it in the command below:

```
 aws ec2 run-instances --image-id <ami id> --security-group-ids <student number>-sg --count 1 --instance-type t2.micro --key-name <student number>-key --query 'Instances[0].InstanceId'

 ```

### [5] Add a tag to your Instance

 ```
  aws ec2 create-tags --resources <Instance Id from above> --tags Key=Name,Value=<student number>
 ```
**NOTE**: If you need to create a single instance, follow the naming format of `<student number>-vm` (e.g., 24242424-vm). If you need to create multiple ones, follow the naming format of `<student number>-vm1` and `<student number>-vm2` (e.g., 24242424-vm1, 24242424-vm2).

### [6] Get the public IP address

```
aws ec2 describe-instances --instance-ids <Instance Id from above> --query 'Reservations[0].Instances[0].PublicIpAddress'
```

### [7] Connect to the instance via ssh
```
ssh -i <student number>-key.pem ubuntu@<IP Address from above>
```

### [8] List the created instance using the AWS console


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
eyJoaXN0b3J5IjpbMjQ3ODg1NzcwLDE0MzYzODQzNjYsLTkxMT
Y0MDYyMCwtMjA4ODc0NjYxMl19
-->