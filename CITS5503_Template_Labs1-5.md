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
<p>Under the <code>`access key</code> tab, create new access key and secret. The region to be selected is <code>eu-north-1</code>` because my student number falls into this region selection.<br>
<img src="http://127.0.0.1/assets/lab1-3.png" alt="enter image description here"></p>
<h2 id="set-up-recent-linux-oses">Set up recent Linux OSes</h2>
<p>

I am running a windows machine, I decided to go with `ubuntus on windows` because it offers an isolated environment and separated file directory, which sets ease with file management.<br>
![enter image description here](http://127.0.0.1/assets/lab1-4.png)

## Install Linux packages

### [1] Install Python 3.10.x
Because my ubuntu version is already `22.04`, I will get the lastest python version which is `3.10.12`.

To update apt to latest version:

    sudo apt update
    sudo apt -y upgrade
![enter image description here](http://127.0.0.1/assets/lab1-5.png)

To check the latest version of python:

    python3 -V
![enter image description here](http://127.0.0.1/assets/lab1-6.png)
 
To install pip3

    sudo apt install -y python3-pip
  
  ![enter image description here](http://127.0.0.1/assets/lab1-7.png)

### [2] Install awscli</h3>
To install AWS CLI and upgrade to latest version

    sudo apt install awscli
    pip3 install awscli --upgrade

![enter image description here](http://127.0.0.1/assets/lab1-8.png)

<h3 id="configure-aws">[3] Configure AWS</h3>
To configure and connect to Amazon EC2

    aws configure
   
  Here we type in the
  ![enter image description here](http://127.0.0.1/assets/lab1-9.png)

<h3 id="install-boto3">[4] Install boto3</h3>
<p>[Refer to the marking rubrics for sufficient step-by-step description.]</p>
<h2 id="test-the-installed-environment">Test the installed environment</h2>
<h3 id="test-the-aws-environment">[1] Test the AWS environment</h3>
<p>[Refer to the marking rubrics for sufficient step-by-step description.]</p>
<h3 id="test-the-python-environment">[2] Test the Python environment</h3>
<p>

[Refer to the marking rubrics for sufficient step-by-step description.]</p>
<h3 id="write-a-python-script">[3] Write a Python script</h3>
<p>

[Refer to the marking rubrics for sufficient step-by-step description.]</p>

<div></div>
<h1 id="lab-2">Lab 2</h1>
<div></div>
<h1 id="lab-3">Lab 3</h1>
<div></div>
<h1 id="lab-4">Lab 4</h1>
<div></div>
<h1 id="lab-5">Lab 5</h1> style="page-break-after: always;"></div>

# Lab 2
<div

<!--stackedit_data:
eyJoaXN0b3J5IjpbNzc0OTY4NTQ1XX0=
-->