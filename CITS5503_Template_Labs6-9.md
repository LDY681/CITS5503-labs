<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">

  <h2>Labs 6-9</h2>
  
  <p>Student ID: [Student ID]24188516</p>
  <p>Student Name: [First and Surname]Dayu Liu</p>

</div>

# Lab 6

## Set up an EC2 instance

### [1] Create an EC2 micro instance with Ubuntu and SSH into it. 
In the first step, we will use the  code in lab2 to create a EC2 instance, stored the access private key, printed out the public IP address. Then we will SSH into the instance by providing the IP address and private key.

In this step, we create an EC2 instance using the **boto3** Python package instead of AWS CLI commands. While the method names and parameters differ, the outcome is the same as in the previous steps. To differentiate this instance from the previous one, we append `-2` to the **Group name**, **Key name**, and **Instance name**.

The following Python script uses `boto3` to create the EC2 **instance, security group, key pair, and instance tag**:

### Workflow

1. **Create Security Group**:  
   The script starts by creating a security group (`24188516-sg-1`) using `ec2.create_security_group()`.
   
2. **Authorize SSH Inbound Rule**:  
   Next, an SSH rule is added using `ec2.authorize_security_group_ingress()`. This allows SSH access on port **22** from all IP addresses (`0.0.0.0/0`).

3. **Create Key Pair**:  
   A key pair (`24188516-key-lab6`) is generated using `ec2.create_key_pair()`, and the private key is saved locally with restricted access permissions using `os.chmod()` to secure it.

4. **Create EC2 Instance**:  
   The script launches an EC2 instance in the specified security group using `ec2.run_instances()`. The **AMI ID** (`ami-07a0715df72e58928`), **instance type** (`t3.micro`), and **key name** (`24188516-key-1`) are provided as parameters.

5. **Tag EC2 Instance**:  
   A name tag (`24188516-vm-1`) is created for the EC2 instance using `ec2.create_tags()`, which helps in identifying the instance easily.

6. **Retrieve Public IP Address**:  
   The public IP address of the newly created EC2 instance is retrieved using `ec2.describe_instances()`.

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

> ### Code Breakdown

1. **`ec2.create_security_group()`**:
   - **`Description`**: Describes the purpose of the security group, here labeled as "security group for development environment".
   - **`GroupName`**: Defines the name of the security group, in this case, `24188516-sg-1`.
  
2. **`ec2.authorize_security_group_ingress()`**:
   - **`GroupName`**: Specifies the security group where the rule will be added, in this case, `24188516-sg-1`.
   - **`IpPermissions`**: This parameter contains the rules that specify what type of inbound traffic is allowed. 
     - **`IpProtocol`**: Defines the protocol, here set to `tcp` for SSH access.
     - **`FromPort` and `ToPort`**: Both set to `22`, defining the SSH port.
     - **`IpRanges`**: Defines the IP range allowed to access the instance. Here, `0.0.0.0/0` allows access from any IP.

3. **`ec2.create_key_pair()`**:
   - **`KeyName`**: Specifies the name of the key pair, here `24188516-key-1`,  generates a new key pair and returns the private key.

4. **`file.write()`**:
   - The private key is saved to a `.pem` file using Python’s built-in File library with the `open()` function, and **`os.chmod()`** is used to set the file’s permission to `400` (read-only).

5. **`ec2.run_instances()`**:
   - **`ImageId`**: Specifies the Amazon Machine Image (AMI) ID, in this case, `ami-07a0715df72e58928`, which contains pre-configured software and settings.
   - **`SecurityGroupIds`**: Lists the security group IDs that will be associated with the instance. Here, the security group is `24188516-sg-1`.
   - **`MinCount` and `MaxCount`**: Define how many instances to launch. only one instance will be created in our case.
   - **`InstanceType`**: Defines the type of instance to launch, in this case, `t3.micro`.
   - **`KeyName`**: Specifies the name of the key pair, `24188516-key-1`, used for SSH access.

6. **`ec2.create_tags()`**:
   - **`Resources`**: Specifies the resources to tag, in this case, the instance ID.
   - **`Tags`**: Defines the key-value pairs for tagging. Here, the tag key is `Name` and the value is `24188516-vm-lab6`, which labels the instance for easier identification.

7. **`ec2.describe_instances()`**:
   - **`InstanceIds`**: Specifies the instance ID to describe details on.
   
![enter image description here](http://127.0.0.1/assets/lab6-1.png)
![enter image description here](http://127.0.0.1/assets/lab6-2.png)

### [2] Install the Python 3 virtual environment package
In this step, we will run the following commands to install virtual environment package and grant sudo permissions to bash operations.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-venv

sudo bash
```
1.  **Update and Upgrade System Packages**:
    -   **`sudo apt-get update`**: Updates the package lists for available or new versions of packages and their dependencies.
    -   **`sudo apt-get upgrade`**: Upgrades the installed packages to the latest versions.
2.  **Install `python3-venv`**:
    -   **`sudo apt-get install python3-venv`**: Installs the `venv` package for Python 3, which is used to create isolated Python environments.
3.  **Switch to Superuser Mode**:
    -   **`sudo bash`**: Elevates the command line session to superuser mode, ensuring all subsequent commands are executed with `sudo` privileges without needing to prepend `sudo` each time. This is helpful when performing multiple operations requiring root access.
  
![enter image description here](http://127.0.0.1/assets/lab6-3.png)

### [3] Access a directory  

Create a directory with a path `/opt/wwc/mysites` and `cd` into the directory.
```
sudo mkdir -p /opt/wwc/mysites
cd /opt/wwc/mysites
```

1. **Create Directories Using `mkdir`**:
   - **`sudo mkdir -p /opt/wwc/mysites`**: Creates the specified directory path (`/opt/wwc/mysites`). The `-p` option ensures that parent directories are created as needed without error if they already exist.

2. **Navigate to the Created Directory**:
   - **`cd /opt/wwc/mysites`**: Changes the working directory to `/opt/wwc/mysites`. This is the directory where subsequent files or projects will be managed.

![enter image description here](http://127.0.0.1/assets/lab6-4.png)

### [4] Set up a virtual environment

```
python3 -m venv myvenv
```

1. **Set Up Virtual Environment**:
   - **`python3 -m venv myvenv`**: Uses Python 3's `venv` module to create a virtual environment named `myvenv` in the current directory (`/opt/wwc/mysites`). This environment will have its own Python interpreter and package directory, isolated from the system's global Python environment.

![enter image description here](http://127.0.0.1/assets/lab6-5.png)

### [5] Activate the virtual environment
In this step, we will activate our virtual environment, install and start Django project and create a Django app
```
source myvenv/bin/activate
pip install django
django-admin startproject lab
cd lab
python3 manage.py startapp polls
```
1. **Activate Virtual Environment**:
   - **`source myvenv/bin/activate`**: Activates the virtual environment `myvenv`, setting the environment for isolated Python package management.

2. **Install Django**:
   - **`pip install django`**: Installs Django into the virtual environment. `pip` is used to fetch the latest version of the Django package.

3. **Start a New Django Project**:
   - **`django-admin startproject lab`**: Uses `django-admin` to create a new Django project named `lab` in the current directory. This generates necessary project files like `manage.py` and a folder structure to build the web application.

4. **Navigate to the Project Directory**:
   - **`cd lab`**: Moves into the project directory to begin working with the Django project files.

5. **Create a New Django App**:
   - **`python3 manage.py startapp polls`**: Uses Django's `manage.py` utility to create a new app called `polls`. The app will have its own views, models, and URLs, encapsulated within the `lab` project.

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
eyJoaXN0b3J5IjpbMTAxOTA2ODUxMCwxMDQ0ODI0MjI1LDEwMj
M5NTUwNywxOTY5OTM3OTI5LDUzMDg3ODY5Nyw5ODk5MjI0MDMs
LTExNDc5NjU3MiwxMDk1NjU0MDIxXX0=
-->