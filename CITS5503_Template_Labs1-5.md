<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">
  <h2>Labs 1-5</h2>
  <p>Student ID: 24188515</p>
  <p>Student Name: Dayu Liu</p>

</div>

# Lab 1

## AWS Account and Log in

### [1] Log into an IAM user account created for you on AWS.
After receiving the email with original login cridentials, I logged-in and reseted my password accordingly.
http://127.0.0.1/assets/lab1-1.png

### [2] Search and open Identity Access Management
Clicked on the top-right panel to access `security cridentials`
http://127.0.0.1/assets/lab1-2.png

<p>Under the `access key` tab, create new access key and secret. Store the key and secret into somewhere private and secure.
http://127.0.0.1/assets/lab1-3.png

## Set up recent Linux OSes
I am running a windows machine, I decided to go with `ubuntus on windows` because it offers an isolated environment and separated file directory, which sets ease with file management.
http://127.0.0.1/assets/lab1-4.png

## Install Linux packages

### [1] Install Python 3.10.x
Because my ubuntu version is already `22.04`, I will get the lastest python version which is `3.10.12`.</p>

To update apt to latest version:
```
sudo apt update
sudo apt -y upgrade
```
http://127.0.0.1/assets/lab1-5.png

To check the latest version of python:
`python3 -V`

http://127.0.0.1/assets/lab1-6.png

To install pip3:

`sudo apt install -y python3-pip`

http://127.0.0.1/assets/lab1-7.png

### [2] Install awscli
To install AWS CLI and upgrade to latest version:
`pip3 install awscli --upgrade`
http://127.0.0.1/assets/lab1-8.png


### [3] Configure AWS
To configure and connect to Amazon EC2:
`aws configure`

http://127.0.0.1/assets/lab1-9.png


### [4] Install boto3
I find this step redundant as `botocore` is already inluded in AWS Cli package, but just for the spirit:
`pip3 install boto3`

http://127.0.0.1/assets/lab1-10.png

## Test the installed environment

### [1] Test the AWS environment
To confirm that we are connected to the `AWS environment`, run a simple command which prints out the region table.
`aws ec2 describe-regions --output table`

http://127.0.0.1/assets/lab1-11.png

### [2] Test the Python environment
We executed a command offered by AWS-Cli in the terminal, now we want to test on the python environment to achive a similar goal:
```
python3
    >>> import boto3
    >>> ec2 = boto3.client('ec2')
    >>> response = ec2.describe_regions()
    >>> print(response)
```

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

  

## [4] get the results

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

<div style="page-break-after: always;"></div>

# Lab 2

<div style="page-break-after: always;"></div>

# Lab 3

<div style="page-break-after: always;"></div>

# Lab 4

<div style="page-break-after: always;"></div>

# Lab 5