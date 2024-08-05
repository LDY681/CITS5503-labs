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
<p><img src="http://127.0.0.1/assets/lab1-10.png" alt="enter image description here"></p>)
<h2 id="test-the-installed-environment">Test the installed environment</h2>
<h3 id="test-the-aws-environment">[1] Test the AWS environment</h3>
To confirm that we are connected to the <code>AWS environment</code>, run a simple command which prints out the region table.
<pre><code>aws ec2 describe-regions --output table
</code></pre>
<p></p><p>ec2 = bt.client(‘ec2’)<br>
response = ec2.describe_regions()<br>
regions = response[‘Regions’]<br>
regions_df = pd.DataFrame(regions)<br>
print(regions_df)<br>
</p>
<p>2| ec2.eu-west-3.amazonaws.com| eu-west-3| opt-in-not-required</p>
<p>
</p><p>3| ec2.eu-west-2.amazonaws.com| eu-west-2| opt-in-not-required</p>
<p>
</p><p>4| ec2.eu-west-1.amazonaws.com| eu-west-1| opt-in-not-required</p>
<p>
</p><p>5| ec2.ap-northeast-3.amazonaws.com| ap-northeast-3| opt-in-not-required</p>
<p>
</p><p>6| ec2.ap-northeast-2.amazonaws.com| ap-northeast-2| opt-in-not-required</p>
<p>
</p><p>7| ec2.ap-northeast-1.amazonaws.com| ap-northeast-1| opt-in-not-required</p>
<p>
</p><p>8| ec2.ca-central-1.amazonaws.com| ca-central-1| opt-in-not-required</p>
<p>
</p><p>9| ec2.sa-east-1.amazonaws.com| sa-east-1| opt-in-not-required</p>
<p>
</p><p>10| ec2.ap-southeast-1.amazonaws.com| ap-southeast-1| opt-in-not-required</p>
<p>
</p><p>11| ec2.ap-southeast-2.amazonaws.com| ap-southeast-2| opt-in-not-required</p>
<p>
</p><p>12| ec2.eu-central-1.amazonaws.com| eu-central-1| opt-in-not-required</p>
<p>
</p><p>13| ec2.us-east-1.amazonaws.com| us-east-1| opt-in-not-required</p>
<p>
</p><p>14| ec2.us-east-2.amazonaws.com| us-east-2| opt-in-not-required</p>
<p>
</p><p>15| ec2.us-west-1.amazonaws.com| us-west-1| opt-in-not-required</p>
<p>
</p><p>16| ec2.us-west-2.amazonaws.com| us-west-2| opt-in-not-required</p>
<h1 id="lab-2">Lab 2</h1>
<div></div>
<h1 id="lab-3">Lab 3</h1>
<div></div>
<h1 id="lab-4">Lab 4</h1>
<div></div>
<h1 id="lab-5">Lab 5</h1> style="page-break-after: always;"&gt;
<h1 id="lab-2">Lab 2</h1>

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE3NjI3MDA5MjRdfQ==
-->