<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">

  <h2>Labs 6-9</h2>
  
  <p>Student ID: [Student ID]24188516</p>
  <p>Student Name: [First and Surname]Dayu Liu</p>

</div>

# Lab 6

## Set up an EC2 instance

### [1] Create an EC2 micro instance with Ubuntu and SSH into it. 
In the first step, we will use the  code in lab2 to create a EC2 instance, stored the access private key, printed out the public IP address. Then we will SSH into the instance by providing the IP address and private key.
```
# createinstance.py
import boto3 as bt
import os

GroupName = '24188516-sg-1'
KeyName = '24188516-key-lab6'
InstanceName= '24188516-vm-1'

ec2 = bt.client('ec2')

# 1 create security group
step1_response = ec2.create_security_group(
    Description="security group for development environment",
    GroupName=GroupName
)

# 2 authorise ssh inbound rule
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

# 3 create key-pair
step3_response = ec2.create_key_pair(KeyName=KeyName)
PrivateKey = step3_response['KeyMaterial']
## save key-pair
with open(f'{KeyName}.pem', 'w') as file:
    file.write(PrivateKey)
## grant file permission
os.chmod(f'{KeyName}.pem', 0o400)

# 4 create instance
step4_response = ec2.run_instances(
    ImageId='ami-07a0715df72e58928',
    SecurityGroupIds=[GroupName],
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName=KeyName
)
InstanceId = step4_response['Instances'][0]['InstanceId']

# 5 create tag
step5_repsonse = ec2.create_tags(
    Resources=[InstanceId],
    Tags=[
        {
            'Key': 'Name',
            'Value': InstanceName
        }
    ]
)

# 6 get IP address
step6_response = ec2.describe_instances(InstanceIds=[InstanceId])

# Extract the public IP address
public_ip_address = step6_response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print(f"{public_ip_address}\n")
```
![enter image description here](http://127.0.0.1/assets/lab6-1.png)
![enter image description here](http://127.0.0.1/assets/lab6-2.png)

### [2] Install the Python 3 virtual environment package

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-venv
```
It is easier now if you change the bash to operate as sudo

```
sudo bash
```
![enter image description here](http://127.0.0.1/assets/lab6-3.png)

### [3] Access a directory  

Create a directory with a path `/opt/wwc/mysites` and `cd` into the directory.
```
sudo mkdir -p /opt/wwc/mysites
cd /opt/wwc/mysites
```
![enter image description here](http://127.0.0.1/assets/lab6-4.png)

### [4] Set up a virtual environment

```
python3 -m venv myvenv
```
![enter image description here](http://127.0.0.1/assets/lab6-5.png)

### [5] Activate the virtual environment

```
source myvenv/bin/activate

pip install django

django-admin startproject lab

cd lab

python3 manage.py startapp polls
```
![enter image description here](http://127.0.0.1/assets/lab6-6.png)
![enter image description here](http://127.0.0.1/assets/lab6-7.png)
**NOTE**: Stop and look at the files that have been created – the project files are to do with the running of the application. We will deal with the files as we go through.


### [6] Install nginx

```
apt install nginx
```
![enter image description here](http://127.0.0.1/assets/lab6-8.png)

### [7] Configure nginx

edit `/etc/nginx/sites-enabled/default` and replace the contents of the file with

```
server {
  listen 80 default_server;
  listen [::]:80 default_server;

  location / {
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Real-IP $remote_addr;

    proxy_pass http://127.0.0.1:8000;
  }
}
```

### [8] Restart nginx

```
service nginx restart
```


### [9] Access your EC2 instance

In your app directory: `/opt/wwc/mysites/lab`, run:

```
python3 manage.py runserver 8000
```

Open a browser and enter the IP address of your EC2 instance. Take a screenshot of what you see and stop your server with CONTROL-C


## Set up Django inside the created EC2 instance

### [1] Edit the following files (create them if not exist)

edit polls/views.py

```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```

edit polls/urls.py 

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

edit lab/urls.py

```
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

### [2] Run the web server again

```
python3 manage.py runserver 8000
```

### [3] Access the EC2 instance

Access the URL: http://\<ip address of your EC2 instance>/polls/, and output what you've got. 

**NOTE**: remember to put the /polls/ on the end and you may need to restart nginx if it does not work.

## Set up an ALB

### [1] Create an application load balancer

Specify the region subnet where your EC2 instance resides.

Create a listener with a default rule Protocol: HTTP and Port 80 forwarding.

Choose the security group, allowing HTTP traffic. 

Add your instance as a registered target.

### [2] Health check

For the target group, specify /polls/ for a path for the health check.

Confirm the health check fetch the /polls/ page every 30 seconds.

### [3] Access

Access the URL: http://\<load balancer dns name>/polls/, and output what you've got.

**NOTE**: When you are done, delete the instance and ALB you created.
<div style="page-break-after: always;"></div>

# Lab 7

<div style="page-break-after: always;"></div>

# Lab 8

<div style="page-break-after: always;"></div>

# Lab 9

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA0NDgyNDIyNSwxMDIzOTU1MDcsMTk2OT
kzNzkyOSw1MzA4Nzg2OTcsOTg5OTIyNDAzLC0xMTQ3OTY1NzIs
MTA5NTY1NDAyMV19
-->