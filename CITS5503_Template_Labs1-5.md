<p></p><div></div><p></p>
  <h2>Labs 1-5</h2>
  <p>Student ID: 24188515</p>
  <p>Student Name: Dayu Liu</p>
<h1 id="lab-1">Lab 1</h1>
<h2 id="aws-account-and-log-in">AWS Account and Log in</h2>
<h3 id="log-into-an-iam-user-account-created-for-you-on-aws.">[1] Log into an IAM user account created for you on AWS.</h3>
<p>After receiving the email with original login cridentials, I logged-in and reseted my password accordingly.<br>
<img src="http://127.0.0.1/assets/lab1-1.png" alt="enter image description here"></p>
<h3 id="search-and-open-identity-access-management">[2] Search and open Identity Access Management</h3>
<p>Clicked on the top-right panel to access <code>security cridentials</code><br>
<img src="http://127.0.0.1/assets/lab1-2.png" alt="enter image description here"></p>
<p>Under the <code>access key</code> tab, create new access key and secret. Store the key and secret into somewhere private and secure.<br>
<img src="http://127.0.0.1/assets/lab1-3.png" alt="enter image description here"></p>
<h2 id="set-up-recent-linux-oses">Set up recent Linux OSes</h2>
<p>
</p><p>
I am running a windows machine, I decided to go with <code>ubuntus on windows</code> because it offers an isolated environment and separated file directory, which sets ease with file management.<br><br>
<img src="http://127.0.0.1/assets/lab1-4.png" alt="enter image description here"></p>
<h2 id="install-linux-packages">Install Linux packages</h2>
<h3 id="install-python-3.10.x">[1] Install Python 3.10.x</h3>
<p>Because my ubuntu version is already <code>22.04</code>, I will get the lastest python version which is <code>3.10.12</code>.</p>
<p>To update apt to latest version:</p>
<pre><code>sudo apt update
sudo apt -y upgrade
</code></pre>
<p><img src="http://127.0.0.1/assets/lab1-5.png" alt="enter image description here"></p>
<p>To check the latest version of python:</p>
<pre><code>python3 -V
</code></pre>
<p><img src="http://127.0.0.1/assets/lab1-6.png" alt="enter image description here"></p>
<p>To install pip3</p>
<pre><code>sudo apt install -y python3-pip
</code></pre>
<p><img src="http://127.0.0.1/assets/lab1-7.png" alt="enter image description here"></p>
<h3 id="install-awsclih3">[2] Install awscli</h3>
<p>To install AWS CLI and upgrade to latest version</p>
<pre><code>sudo apt install awscli
pip3 install awscli --upgrade
</code></pre>
<p><img src="http://127.0.0.1/assets/lab1-8.png" alt="enter image description here"></p>

<h3 id="configure-aws">[3] Configure AWS</h3>
To configure and connect to Amazon EC2
<pre><code>aws configure
</code></pre>
<p>In the prompt, input the <code>access key and secret key</code> we generated.<br>
The region to be selected is <code>eu-north-1</code> because my student number falls into this region range.</p>
<p><img src="http://127.0.0.1/assets/lab1-9.png" alt="enter image description here"></p>
<h3 id="install-boto3">[4] Install boto3</h3>
I find this step redundant as <code>botocore</code> is already inluded in AWS Cli package, but just for the spirit:
<pre><code>pip3 install boto3
</code></pre>

 ![enter image description here](http://127.0.0.1/assets/lab1-10.png)

<h2 id="test-the-installed-environment">Test the installed environment</h2>
<h3 id="test-the-aws-environment">[1] Test the AWS environment</h3>
To confirm that we are connected to the AWS environment, run a simple command which prints out the region table.

    aws ec2 describe-regions --output table
  
  ![enter image description here](http://127.0.0.1/assets/lab1-11.png)

<h3 id="test-the-python-environment">[2] Test the Python environment</h3>
We executed a command offered by AWS-Cli in the terminal, now we want to test on the python environment to achive a similar goal:

    python3
    >>> import boto3
    >>> ec2 = boto3.client('ec2')
    >>> response = ec2.describe_regions()
    >>> print(response)

<h3 id="write-a-python-script">[3] Write a Python script</h3>
Now we create a python script to wrap these lines in one file and also format the reponse into table structure.
The python script is located in ~\cits5503\lab1 in the Ubuntu environment

Run the following code to land in the right lab directory
`cd ./cits5503/lab1`

#### (1) install dependencies
The pandas library is used here to convert un-tabulated data into structured table.
Run the following code to install the extra dependency
`pip install pandas`

#### (2) explain the code
The code in the script adds an extra step, the reponse data is sent as a parameter into pandas dataframe and then gets p
    import boto3 as bt
    import pandas as pd
    
    ec2 = bt.client('ec2')
    response = ec2.describe_regions()
    regions = response['Regions']
    regions_df = pd.DataFrame(regions)
    print(regions_df)

#### (2) run the script
run the following code to execute the python script:
`python3 lab1.py`

  

## [4] get the results

After the script is executed, results are printed in a table structure

  

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

<h1 id="lab-2">Lab 2</h1>
<div></div>
<h1 id="lab-3">Lab 3</h1>
<div></div>
<h1 id="lab-4">Lab 4</h1>
<div></div>
<h1 id="lab-5">Lab 5</h1> style="page-break-after: always;"&gt;
<h1 id="lab-2">Lab 2</h1>

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1NTkxMTIzNzVdfQ==
-->