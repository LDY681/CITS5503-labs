﻿<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">
  <h2>Labs 6-9</h2>
  <p>Student ID: 24188516</p>
  <p>Student Name: Dayu Liu</p>
</div>

# Lab 6

## Set up an EC2 instance

### [1] Create an EC2 micro instance with Ubuntu and SSH into it. 
In the first step, we will use the code in lab2 to create a EC2 instance, stored the access private key, printed out the public IP address. Then we will SSH into the instance by providing the IP address and private key.

In this step, we create an EC2 instance using the **boto3** Python package instead of AWS CLI commands. While the method names and parameters differ, the outcome is the same as in the previous steps. To differentiate this instance from the previous one, we append `-2` to the **Group name**, **Key name**, and **Instance name**.

The following Python script uses `boto3` to create the EC2 **instance, security group, key pair, and instance tag**:

### Workflow
1. **Create Security Group**:  
   The script starts by creating a security group (`24188516-sg-1`) using `ec2.create_security_group()`.
2. **Authorize SSH/HTTP Inbound Rule**:  
   Next, an SSH/HTTP rule is added using `ec2.authorize_security_group_ingress()`. This allows SSH access on port **22** and HTTP access on port **80** from all IP addresses (`0.0.0.0/0`).
3. **Create Key Pair**:  
   A key pair (`24188516-key-lab6`) is generated using `ec2.create_key_pair()`, and the private key is saved locally with restricted access permissions using `os.chmod()` to secure it.
4. **Create EC2 Instance**:  
   The script launches an EC2 instance in the specified security group using `ec2.run_instances()`. The **AMI ID** (`ami-07a0715df72e58928`), **instance type** (`t3.micro`), and **key name** (`24188516-key-lab6`) are provided as parameters.
5. **Tag EC2 Instance**:  
   A name tag (`24188516-vm-1`) is created for the EC2 instance using `ec2.create_tags()`, which helps in identifying the instance easily.
6. **Retrieve Public IP Address**:  
   The public IP address of the newly created EC2 instance is retrieved using `ec2.describe_instances()`.

```
# lab6.py
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
        },
          {
            'IpProtocol': 'http',
            'FromPort': 80,
            'ToPort': 80,
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
     - **`IpProtocol`**: Defines the protocol, here set to `tcp` for SSH access, and `http` for HTTP access.
     - **`FromPort` and `ToPort`**: Set to `22` for the SSH port and `80` for the HTTP port.
     - **`IpRanges`**: Defines the IP range allowed to access the instance. Here, `0.0.0.0/0` allows access from any IP.
3. **`ec2.create_key_pair()`**:
   - **`KeyName`**: Specifies the name of the key pair, here `24188516-key-lab6`,  generates a new key pair and returns the private key.
4. **`file.write()`**:
   - The private key is saved to a `.pem` file using Python’s built-in File library with the `open()` function, and **`os.chmod()`** is used to set the file’s permission to `400` (read-only).
5. **`ec2.run_instances()`**:
   - **`ImageId`**: Specifies the Amazon Machine Image (AMI) ID, in this case, `ami-07a0715df72e58928`, which contains pre-configured software and settings.
   - **`SecurityGroupIds`**: Lists the security group IDs that will be associated with the instance. Here, the security group is `24188516-sg-1`.
   - **`MinCount` and `MaxCount`**: Define how many instances to launch. only one instance will be created in our case.
   - **`InstanceType`**: Defines the type of instance to launch, in this case, `t3.micro`.
   - **`KeyName`**: Specifies the name of the key pair, `24188516-key-lab6`, used for SSH access.
6. **`ec2.create_tags()`**:
   - **`Resources`**: Specifies the resources to tag, in this case, the instance ID.
   - **`Tags`**: Defines the key-value pairs for tagging. Here, the tag key is `Name` and the value is `24188516-vm-lab6`, which labels the instance for easier identification.
7. **`ec2.describe_instances()`**:
   - **`InstanceIds`**: Specifies the instance ID to describe details on.
   
![enter image description here](http://127.0.0.1/assets/lab6-1.png)

Now we can SSH into our instance by accessing `ubuntu@13.61.7.212` and using our generated pem private key.
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
    -   **`update`**: Updates the package lists for available or new versions of packages and their dependencies.
    -   **`upgrade`**: Upgrades the installed packages to the latest versions.
2.  **Install Virtual Environment**:
    -   **`install python3-venv`**: Installs the `venv` package for Python 3, which is used to create isolated Python environments.
3.  **Switch to Superuser Mode**:
    -   **`sudo bash`**: Elevates the command line session to superuser mode, ensuring all subsequent commands are executed with `sudo` privileges without needing to prepend `sudo` each time. 
  
![enter image description here](http://127.0.0.1/assets/lab6-3.png)

### [3] Access a directory  
Now let's make a directory for our app files, create a directory with a path `/opt/wwc/mysites` and `cd` into the directory.
```
sudo mkdir -p /opt/wwc/mysites
cd /opt/wwc/mysites
```

1. **Create Directories Using `mkdir`**:
   - **` mkdir -p`**: Creates the specified directory path (`/opt/wwc/mysites`). The `-p` option ensures that parent directories are created as needed without error if they already exist.

2. **Navigate to the Created Directory**:
   - **`cd /opt/wwc/mysites`**: Changes the working directory to `/opt/wwc/mysites`. This is the directory where our project will be stored.

![enter image description here](http://127.0.0.1/assets/lab6-4.png)


### [4] Set Up a Virtual Environment

To create a new isolated Python environment, run the following command:

```bash
python3 -m venv myvenv
```

#### Key Parameters:

-   **`-m venv`**: Uses the `venv` module to create a new virtual environment.
-   **`myvenv`**: Specifies the name of the directory to store the virtual environment. 

This command will create a new directory called `myvenv` containing the Python interpreter, standard library, and other resources, allowing us to manage dependencies separately from the global Python environment.
![enter image description here](http://127.0.0.1/assets/lab6-5.png)

### [5] Source the virtual environment
In this step, we will activate our virtual environment, install and start the Django project and create a Django app
```
source myvenv/bin/activate
pip install django
django-admin startproject lab
cd lab
python3 manage.py startapp polls
```

1. **Source Virtual Environment**:
   - **`source myvenv/bin/activate`**: Activates the virtual environment `myvenv`, setting the environment for isolated Python package management.
2. **Install Django**:
   - **`pip install django`**: Installs Django into the virtual environment.
3. **Start a New Django Project**:
   - **`django-admin startproject lab`**: Uses `django-admin` to create a new Django project named `lab` in the current directory. This generates necessary project files like `manage.py` and a folder structure to build the web application.
4. **Create a New Django App**:
   - **`python3 manage.py startapp polls`**: Uses Django's `manage.py` utility to create a new app called `polls`. We can see that the `polls` app will have its own views, models, and URLs.

![enter image description here](http://127.0.0.1/assets/lab6-6.png)
![enter image description here](http://127.0.0.1/assets/lab6-7.png)

> ### File Structure
Once the commands are executed, Django creates the following structure for our project:
- **`lab/`**: The project directory containing the settings and configurations for the entire Django project.
  - **`__init__.py`**: Marks the directory as a Python package.
  - **`settings.py`**: Contains project settings such as installed apps, middleware, and database configurations.
  - **`urls.py`**: The project's URL declarations for routing HTTP requests.
  - **`wsgi.py`**: The entry point for WSGI-compatible web servers to serve our project.
  - **`asgi.py`**: The entry point for ASGI-compatible servers for asynchronous support.
- **`manage.py`**: A command-line utility to interact with the Django project (e.g., running the server, creating migrations).

- **`polls/`**: The app directory that houses the `polls` app created using `startapp`.
  - **`migrations/`**: Directory for database migrations files.
  - **`admin.py`**: For registering models with the Django admin.
  - **`apps.py`**: Configuration for the app itself.
  - **`models.py`**: Where database models are defined.
  - **`tests.py`**: Houses unit tests for the app.
  - **`views.py`**: Where request-handling functions and classes are defined.

The files created by Django provide a boilerplate for developing the project. In the later part, we will work on the poll files to build a simple `"Hello, World"` page.


### [6] Install Nginx
To install the Nginx web server, run the following command:
```bash
apt install nginx
```
#### Key Parameters:
-   **`nginx`**: Installs the `nginx` package from the repository.

This command sets up the Nginx web server, which can be used as a reverse proxy for our applications.
![enter image description here](http://127.0.0.1/assets/lab6-8.png)

### [7] Configure nginx
To configure Nginx to work as a reverse proxy for our Django application, go to the Nginx configuration file located at `/etc/nginx/sites-enabled/default` and add the following.
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
#### Key Parameters:
- **`listen 80`**: Specifies the port Nginx listens on. Here, **80** is the default HTTP port for web traffic. The second `listen` line is for IPv6.
- **`proxy_set_header X-Forwarded-Host $host;`**: Sets the `X-Forwarded-Host` header to the host of the original request. This header preserves the original `Host` header sent by the client.
- **`proxy_set_header X-Real-IP $remote_addr;`**: Sets the `X-Real-IP` header to the real client IP address. This header helps in passing the original client's IP address to the proxied server.
- **`proxy_pass http://127.0.0.1:8000;`**: Forwards incoming traffic to `http://127.0.0.1:8000`, where our Django application is running. This allows Nginx to act as a reverse proxy, handling requests and passing them to our Django server.

This configuration ensures that all incoming traffic to our server's port **80** is passed to the Django app running locally on port **8000**.

### [8] Restart nginx
To apply our new configuration, we need to restart the Nginx service, run the following command:
```
service nginx restart
```
#### Key Parameters:
-   **`service`**: Manages system services.
-   **`nginx`**: Specifies the Nginx service to be managed.
-   **`restart`**: Restarts the Nginx service, stopping smf then starting it again to apply configuration changes.

This command ensures that any updates or changes made to the Nginx configuration are applied.

### [9] Access our EC2 instance

In the app directory `/opt/wwc/mysites/lab`, run the following command to start our Django application server on port **8000**:

```
python3 manage.py runserver 8000
```
#### Key Parameters:
-   **`python3 manage.py `**: Runs the script to launch the Django server.
-   **`runserver 8000`**: Specifies the port on which the server will listen for requests. In this case, it's **8000**.

We can now access the web app via `http://13.61.7.212`.
![enter image description here](http://127.0.0.1/assets/lab6-9.png)

## Set up Django App
In this step, we will modify the Django App to display a simple "Hello, World" message when visiting the `/polls` route and display the admin interface when visiting `/admin` page.

### [1] Edit `polls/view.py`
In `polls/views.py`, create a view that returns a simple HTTP response "Hello World":
```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```
-   **`HttpResponse`**: Returns a simple HTTP response containing the string `"Hello, world."`.

In `polls/urls.py`, map the URL pattern to the view created above:

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

-   **`path('', views.index, name='index')`**: Routes the root URL of the `polls` app to the `index` view function.

In `lab/urls.py`, include the `polls` app URLs and set up the admin interface:
```
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```
-   **`include('polls.urls')`**: Includes the `polls` app's URL configurations under the path `polls/`.
-   **`admin.site.urls`**: Sets up the admin interface under the path `admin/`.

### [2] Restart the web server
Now we can apply the changes and restart the server to see the changes.
```
python3 manage.py runserver 8000
```
#### Key Parameters:

-   **`python3 manage.py`**: Runs the script to launch the Django server.
-   **`runserver 8000`**: Specifies the port on which the server will listen for requests. In this case, it’s  **8000**.

### [3] Access the EC2 instance
We can access the polls index page with `Hello,World` message by visiting `http://13.61.7.212/polls/`. ![enter image description here](http://127.0.0.1/assets/lab6-10.png)

We can access the built-in admin module by visiting `http://13.61.7.212/admin/`
![enter image description here](http://127.0.0.1/assets/lab6-11.png)

## Set up an ALB
### [1] Create an application load balancer & Health check
We will use the code in `lab5` as a start to create the load balancer, the only difference is this time we apply a health check on the `/polls/` path of our hosted website every 30 seconds.

### Workflow
1. **Initialize Clients and Define Variables**:
   - Uses **boto3** to initialize EC2 and Elastic Load Balancing (ELBv2) clients.
   - Defines constants for security group, key pair, instance ID, load balancer name, and target group name.
2. **Fetch Subnets for the EC2 Instance**:
   - Retrieves subnets in the `eu-north-1` region for the load balancer.
3. **Create Application Load Balancer**:
   - Uses **`elbv2.create_load_balancer()`** to create an ALB in the specified subnets, using the security group to allow HTTP traffic.
4. **Create Target Group for Health Checks**:
   - Uses **`elbv2.create_target_group()`** to create a target group for the EC2 instance.
   - Specifies HTTP as the protocol and port 80 for forwarding.
   - Sets up a DNS health check on the `/polls/` path to be performed every 30 seconds.
5. **Register EC2 Instances as Targets**:
   - Registers the EC2 instance to the target group using **`elbv2.register_targets()`**.
6. **Create Listener for the Load Balancer**:
   - Sets up a listener on port 80 to forward HTTP requests to the target group using **`elbv2.create_listener()`**.
 
```
import boto3 as bt
import os

GroupId = 'sg-0ef7af6d7bf260d42'
KeyName = '24188516-key-lab6'
InstanceId = 'i-039c0b853dc14f418'
LoadBalancerName = '24188516-elb'
TargetGroupName = '24188516-tg'

# Initialize EC2 and ELBv2 clients
ec2 = bt.client('ec2', region_name='eu-north-1')
elbv2 = bt.client('elbv2')

subnet_response = ec2.describe_subnets()['Subnets']
Subnets = [subnet['SubnetId'] for subnet in subnet_response]

# 6. Create application load balancer
loadbalancer_response = elbv2.create_load_balancer(
    Name=LoadBalancerName,
    Subnets=Subnets,
    SecurityGroups=[GroupId],
    Scheme='internet-facing',
    Type='application'
)
LoadBalancerArn = loadbalancer_response['LoadBalancers'][0]['LoadBalancerArn']
LoadBalancerDnsName = loadbalancer_response['LoadBalancers'][0]['DNSName']

# 7. Create target group
VpcId = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
targetgroup_response = elbv2.create_target_group(
    Name=TargetGroupName,
    Protocol='HTTP',
    Port=80,
    VpcId=VpcId,
    TargetType='instance',
    HealthCheckProtocol='HTTP',
    HealthCheckPort='80',
    HealthCheckPath='/polls/',
    HealthCheckIntervalSeconds=30
)
TargetGroupArn = targetgroup_response['TargetGroups'][0]['TargetGroupArn']

# 8. Register instances as targets
elbv2.register_targets(
    TargetGroupArn=TargetGroupArn,
    Targets=[{'Id': InstanceId}]
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
print(f"Instance ID: {InstanceId}")
print(f"Load Balancer ARN: {LoadBalancerArn}")
print(f"Target Group ARN: {TargetGroupArn}")
print(f"Load Balancer DNS Name: {LoadBalancerDnsName}")
```
> ### Code Breakdown
1.  **`elbv2.create_load_balancer()`**: Creates an internet-facing application load balancer.
    -   **`Name`**: Specifies the name of the load balancer.
    -   **`Subnets`**: Provides the subnets across which the load balancer will distribute traffic.
    -   **`SecurityGroups`**: Attaches the security group to the load balancer for traffic control.
    -   **`Scheme`**: Specifies that the load balancer is internet-facing.
    -   **`Type`**: Sets the type of load balancer as `application`.
2.  **`elbv2.create_target_group()`**: Sets up a target group for the load balancer with a health check.
    -   **`Name`**: The name of the target group.
    -   **`Protocol`** and **`Port`**: Specifies HTTP and port 80 for forwarding requests.
    -   **`VpcId`**: ID of the VPC that hosts the EC2 instances.
    -   **`HealthCheckProtocol`** and **`HealthCheckPort`**: Specifies HTTP protocol and port 80 for health checks.
    -   **`HealthCheckPath`**: The path for health checks (`/polls/`).
    -   **`HealthCheckIntervalSeconds`**: Interval for health checks (30 seconds).
3.  **`elbv2.register_targets()`**: Registers the specified EC2 instance to the target group.
    -   **`TargetGroupArn`**: ARN of the target group to register targets.
    -   **`Targets`**: List of target instance IDs to be registered.
4.  **`elbv2.create_listener()`**: Creates a listener to route incoming HTTP traffic on port 80.
    -   **`LoadBalancerArn`**: ARN of the load balancer to attach the listener.
    -   **`Protocol`** and **`Port`**: Specifies HTTP protocol and port 80 for listening.
    -   **`DefaultActions`**: Defines actions for forwarding requests to the target group.

After the load balancer is initialized and up in action, we can go to AWS console and see the result of health check.
![enter image description here](http://127.0.0.1/assets/lab6-14.png)

### [3] Access the mapped DNS name
We can get the ALB's DNS name from `print(f"Load Balancer DNS Name: {LoadBalancerDnsName}")`.
![enter image description here](http://127.0.0.1/assets/lab6-12.png)

Now we can access its url with path `/polls/` to see if the mapping works properly: http://24188516-elb-920225157.eu-north-1.elb.amazonaws.com/polls/
![enter image description here](http://127.0.0.1/assets/lab6-13.png)

<div style="page-break-after: always;"></div>

# Lab 7
## Set up Fabric Connection
### [1] Create EC2 Instance
In the first step, we use our script from **Lab 6** to create a new EC2 instance. We will not elaborate on the code base because it's already covered in previous lab. Run the following command in our local Ubuntu machine:
```
python3 createinstance.py
```
This script automates the creation of the EC2 instance with the required configuration for SSH access and HTTP access. After the instance is successfully created, we retrieve the public IP address.

![enter image description here](http://127.0.0.1/assets/lab7-1.png)

### [2] Install Fabric
In this step, we install the **Fabric** package, which is used for automating SSH-based tasks such as managing remote servers.
`pip install fabric` 
#### Key Parameters:
-   **`fabric`**: Installs the Fabric package, enabling us to automate remote server management and deployment tasks.

![enter image description here](http://127.0.0.1/assets/lab7-2.png)


### [3] Configure Fabric
To enable Fabric to connect to our EC2 instance, we need to configure an SSH connection by creating a config file at `~/.ssh/config`. This configuration file stores connection details such as the host, IP address, and identity file. Use `vi ~/.ssh/config` to open the config file and edit as following:
```
Host 24188516-vm-1
	Hostname 16.171.206.115
	User ubuntu
	UserKnownHostsFile /dev/null
	StrictHostKeyChecking no
	PasswordAuthentication no
	IdentityFile /home/liudayubob/cits5503/lab7/24188516-key-lab7.pem
``` 
#### Key Parameters:
1.  **`Host`**: Defines the alias for our EC2 instance, which will be used when calling the Fabric connection function.
2.  **`Hostname`**: Specifies the public IP address (in this case, `16.171.206.115`) of our EC2 instance.
3.  **`User ubuntu`**: The default username for EC2 instances based on the Ubuntu AMI image.
4.  **`IdentityFile`**: The path to our private key file (generated during instance creation) for authentication.
5.  **`UserKnownHostsFile /dev/null` and `StrictHostKeyChecking no`**: These disable SSH host key checking, preventing the need for manual approval when connecting.

By creating a host configuration, we can use Fabric to connect to the EC2 instance without needing to specify credentials on every connection.
![enter image description here](http://127.0.0.1/assets/lab7-3.png)


### [4] Test Fabric Connection
We will use the following Fabric code to establish a connection to the EC2 instance. Fabric looks up the host file and uses the connection configuration for `24188516-vm-1`. After establishing the connection, we will run a simple command to verify it.

The command `c.run('uname -s')` will return "Linux" as output, confirming that the connection is successful and commands can be executed on the instance. 
```
python3
>>> from fabric import Connection
>>> c = Connection('24188516-vm-1')
>>> result = c.run('uname -s')
Linux
``` 
#### Key Parameters:
-   **`Connection()`**: Uses the SSH configuration to connect to the EC2 instance using the alias `24188516-vm-1`.
-   **`c.run('uname -s')`**: Runs the `uname -s` command, confirming the operating system on the remote instance is Linux.

![enter image description here](http://127.0.0.1/assets/lab7-4.png)

## Automation for creating Django App
In this section, we will automate the process of setting up a Python virtual environment, configuring Nginx, and creating a Django app within the EC2 instance using Fabric.
The commands from **Lab 6** will be converted to Fabric's `c.run()` for regular commands and `c.sudo()` for commands requiring admin privileges.
Additionally, file editing will be handled using `echo`. We will use file I/O to write Nginx configuration to avoid issues with `$` placeholders.
Due to the fact that each  `c.run()` command is runned isolately, to persist the sourced virtual environment, we will re-source the environment before running further commands.

### Workflow:
1. **Install Packages**:
   - Update and upgrade system packages.
   - Install the Python virtual environment package (`python3-venv`).
   - Install Nginx web server.
2. **Set Up Virtual Environment**:
   - Create a project directory and assign necessary permissions.
   - Set up a virtual environment within the project directory and install Django.
3. **Create Django Project and App**:
   - Start a new Django project and app (`polls`) inside the virtual environment.
   - Modify the views, URLs, and settings to display "Hello, world" from the `polls` app.
4. **Configure Nginx Server**:
   - Write a new Nginx configuration file to act as a reverse proxy, forwarding traffic from port 80 to the Django app running on port 8000.
5. **Run Django Server**:
   - Run the Django development server in the background, ensuring the app is accessible on port 8000.

Here is the script that automates these steps:
```python
from fabric import Connection

EC2_INSTANCE_NAME = '24188516-vm-1'
PROJECT_DIR = '/opt/wwc/mysites/lab'

def install_prerequisites(c):
    # Update and upgrade system packages
    c.sudo('apt-get update -y')
    c.sudo('apt-get upgrade -y')
    c.sudo('apt-get install python3-venv -y')
    c.sudo('apt install nginx -y')

def set_virtual_env(c):
    # Create project directory and navigate to it
    c.sudo(f'mkdir -p {PROJECT_DIR}')
    # Grant permissions to user
    c.sudo(f'chown -R ubuntu:ubuntu {PROJECT_DIR}')
    # Create env and source env
    c.run(f'cd {PROJECT_DIR} && python3 -m venv myvenv')
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && pip install django')

def setup_django_app(c):
    # Need to cd and source env again
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && django-admin startproject lab .')
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && python3 manage.py startapp polls')

    # Polls app
    c.run(f'echo "from django.http import HttpResponse" > {PROJECT_DIR}/polls/views.py')
	c.run(f'echo "def index(request): return HttpResponse(\'Hello, world.\')" >> {PROJECT_DIR}/polls/views.py')
    
	# Admin app and routing
    c.run(f'echo "from django.urls import path\nfrom . import views\nurlpatterns = [path(\'\', views.index, name=\'index\')]" > {PROJECT_DIR}/polls/urls.py')
	c.run(f'echo "from django.urls import include, path\nfrom django.contrib import admin\nurlpatterns = [path(\'polls/\', include(\'polls.urls\')), path(\'admin/\', admin.site.urls)]" > {PROJECT_DIR}/lab/urls.py')

def configure_nginx(c):
    nginx_config = '''
    server {
      listen 80 default_server;
      listen [::]:80 default_server;

      location / {
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        proxy_pass http://127.0.0.1:8000;
      }
    }
    '''
    
    # Write the nginx config locally and upload ($placholder were messed up with echo)
    with open("nginx_temp.conf", "w") as f:
        f.write(nginx_config)
    c.put("nginx_temp.conf", "/tmp/nginx_temp.conf")
    c.sudo('mv /tmp/nginx_temp.conf /etc/nginx/sites-enabled/default')
    
    # Restart Nginx to apply changes
    c.sudo('service nginx restart')

def run_django_server(c):
    # Start Django development server in the background
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && python3 manage.py runserver 8000')

if __name__ == "__main__":
    fabric = Connection(EC2_INSTANCE_NAME)

    install_prerequisites(fabric)
    set_virtual_env(fabric)
    setup_django_app(fabric)
    configure_nginx(fabric)
    run_django_server(fabric)
```
> ### Code Breakdown:
1.  **`Install_prerequisites()`**:
    -   **`apt-get update`** and **`apt-get upgrade`**: Updates and upgrades system packages.
    -   **`apt-get install python3-venv`**: Installs Python 3's virtual environment tool.
    -   **`apt install nginx`**: Installs the Nginx web server for handling HTTP traffic.
2.  **`Set_virtual_env()`**:
    -   **`mkdir -p`**: Creates the project directory to store our virtual environment settings and django app.
    -   **`python3 -m venv myvenv`**: Creates a virtual environment.
    -   **`pip install django`**: Installs Django in the virtual environment.
3.  **`Setup_django_app()`**:
    -   **`django-admin startproject lab`**: Creates the Django project named `lab`.
    -   **`python3 manage.py startapp polls`**: Creates the `polls` app.
    -   **`echo XXX`**: Writes the `views.py`, `urls.py`, and `lab/urls.py` with proper HTML contents and routings for displaying "Hello, world" page and the admin app.
4.  **`Configure_nginx()`**:
    -   **`nginx_config = {}`**: Writes a configuration file to forward requests from port **80** to Django on port **8000**.
    -   **`service nginx restart`**: Restarts Nginx to apply the changes.
5.  **`Run_django_server()`**:
    -   **`manage.py runserver`**: Runs the Django server on port 8000.
![enter image description here](http://127.0.0.1/assets/lab7-5.png)

Now with the Django App started and the server is online, we can go to `/admin/` and `/polls` to verify it's working properly.
![enter image description here](http://127.0.0.1/assets/lab7-6.png)
![enter image description here](http://127.0.0.1/assets/lab7-7.png)
<div style="page-break-after: always;"></div>

# Lab 8
## Install and Run Jupyter Notebooks
In this step, we will install Jupyter Notebooks and use it for AI training. Jupyter Notebooks provide an interactive environment to run Python code on the go.

```bash
pip install notebook
jupyter notebook
```
- **`pip install notebook`**: Installs the Jupyter Notebook package
-   **`jupyter notebook`**: Starts the Jupyter Notebook server and opens a web interface in our browser. It launches at `http://127.0.0.1:8889` in our case, because the default port is already in use.

![enter image description here](http://127.0.0.1/assets/lab8-1.png)

After running the above commands,  we can see that the Jupyter server has launched, and the `labAI.ipynb` notebook file is visible on the file server interface.
![enter image description here](http://127.0.0.1/assets/lab8-3.png)

## Install ipykernel
In this step, we will install the `ipykernel` package, this is the kernel package for Python coding in Jupyter Notebooks. 
```
pip install ipykernel
```
- **`ipykernel`**: This package allows Jupyter to communicate with the Python interpreter. 

![enter image description here](http://127.0.0.1/assets/lab8-2.png)

## Necessary Changes
In this section, we will modify the provided code `LabAI.ipynb` within the Jupyter notebook to make it work in our environment.

### [1] Modify Region, Student ID, and Bucket Name
Let's update the constants for the AWS region, our student ID, and the name of the S3 bucket where the dataset will be stored. This creates a personalized setup for the job.
```
region = 'eu-north-1'  # use the region us are mapped to
student_id = "24188516"  # use our student ID
bucket = '24188516-lab8'  # use <studentid-lab8> as our bucket name
```
### [2] Create an S3 Bucket
We will also create an S3 bucket to store the training and testing datasets. Here, we use the `boto3` library to create a bucket in the specified region `eu-north-1` and add an object with the prefix for our folder destination.
```
s3 = boto3.client('s3', region_name=region)
bucket_config = {'LocationConstraint': region}
s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=bucket_config)  # Create the bucket in our region
s3.put_object(Bucket=bucket, Key=f"{prefix}/")  # Create a folder object with the prefix
```

### [3] Convert Non-numerical Values (True/False to 1/0)
Because our tunning job can't handle non-numerical values, after reading the dataset and before splitting it into training/testing set, we will traverse the model_data and convert all datas to numeric ones.
```
# Change True/False to 1/0
model_data = model_data.replace({True: 1, False: 0})
```

### [4] Running the Notebook
After making the necessary changes to the notebook, we can execute the notebook by navigating to the **Run** menu and selecting **Run All Cells/ Run Selected Cells**.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab8-4.png)

## Dataset Q&A
Read the dataset into a Pandas data frame and answer the following two questions:
	#1. Which variables in the dataset are categorical? Give at least four variables.
	#2. Which variables in the dataset are numerical? Give at least four variables.
```
After inspecting the dataframe, we can get the following conclusions:
#1: Categorical Variables: job, martial, education, contact
#2: Numerical Variables: age, duration, nr.employed, euribor3m 
```

## AI Training
In ``LabAI.ipynb``, we will set up a tuning job using Amazon SageMaker. Steps involve installing the necessary libraries, preparing data, and running a hyperparameter tuning job using XGBoost. The final objective is to use SageMaker for training a model on the Bank Marketing dataset.

###  [1]  Install Required Libraries
To begin, we need to install several essential libraries such as SageMaker, Pandas, and Numpy for machine learning and data processing.
1.  **Install SageMaker**:
    -   SageMaker is required to create and manage training jobs, models, and endpoints in AWS.
2.  **Install Pandas and Numpy**:
    -   Pandas is used for data manipulation, while Numpy is used for numerical operations.
```
# Install SageMaker via Jupyter Notebook
!pip install sagemaker

# Install Pandas and Numpy via Jupyter Notebook
!pip install pandas
!pip install numpy
```

###  [2] Prepare SageMaker Session and S3 Bucket
We need to set up a SageMaker session, IAM role, and S3 bucket to store the training data.

#### Workflow
1.  **Set up SageMaker Session**:
    -   Initialize the SageMaker and IAM clients, set the region, and get the ARN of the SageMaker role.
2.  **Create an S3 Bucket**:
    -   Create an S3 bucket to store training data.
3.  **Download Dataset**:
    -   Download and unzip the Bank Marketing dataset from UCI ML repository.
```
import sagemaker
import boto3
import numpy as np
import pandas as pd

region = 'eu-north-1'  # Set our AWS region
smclient = boto3.Session(region_name=region).client("sagemaker")
iam = boto3.client('iam', region_name=region)
sagemaker_role = iam.get_role(RoleName='SageMakerRole')['Role']['Arn']
student_id = "24188516"  # Use our student ID
bucket = '24188516-lab8'  # Use our student ID for bucket name
prefix = f"sagemaker/{student_id}-hpo-xgboost-dm"

# Create an S3 bucket and folder
s3 = boto3.client('s3', region_name=region)
bucket_config = {'LocationConstraint': region}
s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=bucket_config)  # Create bucket
s3.put_object(Bucket=bucket, Key=f"{prefix}/")  # Create a folder in S3

# Download dataset
!wget -N https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip
!unzip -o bank-additional.zip
```
> #### Code Breakdown:
-   **`sagemaker.Session()`**: Initializes a SageMaker session to interact with AWS SageMaker services.
-   **`boto3.client('s3')`**: Creates an S3 client to interact with S3 services.
-   **`s3.create_bucket()`**: Creates an S3 bucket in the specified region.
-   **`s3.put_object()`**: Creates a folder inside the S3 bucket for storing data.
-   **`!wget`** and **`!unzip`**: Downloads and unzips the dataset to our local folder.

We can see that our folder has been created in the S3 bucket.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab8-5.png)

The dataset has been downloaded and uncompressed.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab8-9.png)

###  [3] Data Preparation and Processing
We will prepare the dataset for training by converting categorical data to binary indicators and splitting the data into training, validation, and test sets.


#### Workflow
1. **Load and Process Data**: 
	- Load the dataset into Pandas and create new indicator columns for specific variables.
2.  **Convert to Dummy Variables**:
    -   Convert categorical variables into sets of indicators using `pd.get_dummies()`.
3.  **Remove Unnecessary Columns**:
    -   Drop economic variables and duration from the dataset to avoid bias in future predictions.
4.  **Fix Non-Numeric Data**:
    -   Replace `True/False` values with `1/0` to avoid non-numeric errors in SageMaker.
5.  **Split Train/Validation/Test Data**:
    -   Split the data into training (70%), validation (20%), and test (10%) datasets.
6.  **Save Split Datasets as CSV Files**:
    -   Save each split as a CSV file, removing headers and adjusting the first column to be the target variable.
7.  **Upload the Datasets to S3**:
    -   Upload the processed datasets to S3 to allow SageMaker to access them during training.

```
# Load dataset into Pandas
data = pd.read_csv("./bank-additional/bank-additional-full.csv", sep=";")

# Add new indicator columns
data["no_previous_contact"] = np.where(data["pdays"] == 999, 1, 0)
data["not_working"] = np.where(np.in1d(data["job"], ["student", "retired", "unemployed"]), 1, 0)

# Convert categorical variables to dummy variables
model_data = pd.get_dummies(data)

# Remove unnecessary columns
model_data = model_data.drop(
    ["duration", "emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"],
    axis=1,
)

# Replace True/False with 1/0
model_data = model_data.replace({True: 1, False: 0})

# Split data into training, validation, and test datasets
train_data, validation_data, test_data = np.split(
    model_data.sample(frac=1, random_state=1729),
    [int(0.7 * len(model_data)), int(0.9 * len(model_data))],
)

# Save datasets as CSV files
pd.concat([train_data["y_yes"], train_data.drop(["y_no", "y_yes"], axis=1)], axis=1).to_csv(
    "train.csv", index=False, header=False
)
pd.concat([validation_data["y_yes"], validation_data.drop(["y_no", "y_yes"], axis=1)], axis=1).to_csv(
    "validation.csv", index=False, header=False
)
pd.concat([test_data["y_yes"], test_data.drop(["y_no", "y_yes"], axis=1)], axis=1).to_csv(
    "test.csv", index=False, header=False
)

# Upload the datasets to S3
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "train/train.csv")
).upload_file("train.csv")
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "validation/validation.csv")
).upload_file("validation.csv")
``` 
> #### Code Breakdown:
- **`pd.read_csv()`**: Reads the dataset into a Pandas DataFrame from the given file.
- **`np.where()`**: Adds indicator columns based on specific conditions (e.g., checking if a customer was previously contacted).
- **`pd.get_dummies()`**: Converts categorical variables into dummy variables, making them suitable for machine learning models.
- **`model_data.drop()`**: Removes unnecessary columns that could introduce bias or noise into the model.
- **`model_data.replace()`**: Replaces `True/False` values with `1/0` to avoid non-numeric errors during SageMaker training.
- **`np.split()`**: Randomly splits the dataset into training, validation, and test sets based on specified proportions.
- **`pd.concat()`**: Combines the target column (`y_yes`) with the remaining feature columns and saves them as CSV files for each split.
- **`os.path.join()`**: Combines the bucket name and the prefix to create the correct path for uploading files to S3.
- **`Object.upload_file()`**: Uploads the prepared training and validation CSV files to the specified S3 bucket to use during training.

We can see that the dataset have been created and uploaded to our designated directories in the S3 bucket.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab8-6.png)
![Jupyter Notebook Running](http://127.0.0.1/assets/lab8-7.png)

###  [4]  Set Up Hyperparameter Tuning Job
Next, we'll configure and launch a hyperparameter tuning job using SageMaker's XGBoost algorithm.

#### Workflow
1.  **Configure Hyperparameters**:
    -   Define a set of hyperparameter ranges that will be tuned using SageMaker. These include parameters like `eta` (learning rate), `min_child_weight`, `alpha` and `max_depth`.
    -   Set the resource limits and specify that the objective is to maximize the area under the curve (AUC) for validation data.
2.  **Specify Training Job**:
    -   Specify the training algorithm (XGBoost), input data (from S3), and the resource attributes (instance type, count, and storage).
    -   Set a stopping condition to ensure the training job doesn't run indefinitely and define static hyperparameters like `eval_metric` and `objective`.
3.  **Launch Hyperparameter Tuning**:
    -   Use the SageMaker APIs to launch the hyperparameter tuning job, train multiple models and return the best one based on the defined metric (`validation:auc`).

```
from time import gmtime, strftime, sleep
from sagemaker.image_uris import retrieve

# Set up a unique tuning job name
tuning_job_name = f"{student_id}-xgboost-tuningjob-01"
print(tuning_job_name)

# Hyperparameter ranges for tuning
tuning_job_config = {
    "ParameterRanges": {
        "ContinuousParameterRanges": [
            {"Name": "eta", "MinValue": "0", "MaxValue": "1"},
            {"Name": "min_child_weight", "MinValue": "1", "MaxValue": "10"},
            {"Name": "alpha", "MinValue": "0", "MaxValue": "2"},
        ],
        "IntegerParameterRanges": [{"Name": "max_depth", "MinValue": "1", "MaxValue": "10"}],
    },
    "ResourceLimits": {"MaxNumberOfTrainingJobs": 2, "MaxParallelTrainingJobs": 2},
    "Strategy": "Bayesian",
    "HyperParameterTuningJobObjective": {"MetricName": "validation:auc", "Type": "Maximize"},
}

# Specify XGBoost algorithm for training
training_image = retrieve(framework="xgboost", region=region, version="latest")
s3_input_train = f"s3://{bucket}/{prefix}/train"
s3_input_validation = f"s3://{bucket}/{prefix}/validation/"

training_job_definition = {
    "AlgorithmSpecification": {"TrainingImage": training_image, "TrainingInputMode": "File"},
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "DataSource": {"S3DataSource": {"S3Uri": s3_input_train, "S3DataType": "S3Prefix"}},
        },
        {
            "ChannelName": "validation",
            "DataSource": {"S3DataSource": {"S3Uri": s3_input_validation, "S3DataType": "S3Prefix"}},
        },
    ],
    "OutputDataConfig": {"S3OutputPath": f"s3://{bucket}/{prefix}/output"},
    "ResourceConfig": {"InstanceCount": 1, "InstanceType": "ml.m5.xlarge", "VolumeSizeInGB": 10},
    "RoleArn": sagemaker_role,
    "StoppingCondition": {"MaxRuntimeInSeconds": 43200},
    "StaticHyperParameters": {"eval_metric": "auc", "num_round": "1", "objective": "binary:logistic"}, }

# Launch the hyperparameter tuning jobsmclient.create_hyper_parameter_tuning_job(
	HyperParameterTuningJobName=tuning_job_name,
	HyperParameterTuningJobConfig=tuning_job_config,
	TrainingJobDefinition=training_job_definition,
)
```  
> #### Code Breakdown:
1.  **`tuning_job_config = {}`**:
    -   **`ParameterRanges`**: Defines the range of hyperparameters to be optimized. 
    -   **`ResourceLimits`**: Restricts the number of training jobs to 2, both for maximum jobs and parallel jobs.
    -   **`Strategy`**: Specifies that SageMaker will use Bayesian optimization to explore the hyperparameter space.
    -   **`HyperParameterTuningJobObjective`**: Sets the objective to maximize the area under the ROC curve (AUC) on the validation dataset.
2.  **`retrieve()`**: Retrieves the latest version of the XGBoost container image from SageMaker for the specified region.
3.  **`training_job_definition = {}`**:
    -   **`AlgorithmSpecification`**: Specifies the XGBoost algorithm and the input mode (File-based input).
    -   **`InputDataConfig`**: Specifies the paths in S3 where the training and validation data are stored.
    -   **`OutputDataConfig`**: Defines the S3 location where the training job outputs will be saved.
    -   **`ResourceConfig`**: Configures the compute resources for the training job, including the instance type, instance count, and storage.
    -   **`StoppingCondition`**: Limits the maximum run time of the training job to 12 hours (43,200 seconds).
    -   **`StaticHyperParameters`**: Sets fixed hyperparameters that are not tuned, such as `objective` (binary classification) and `eval_metric` (AUC).
4.  **`create_hyper_parameter_tuning_job()`**: Launches the tuning job using the defined configuration.

###  [5]  Monitor Hyperparameter Tuning Job
After launching the hyperparameter tuning job, we can monitor its progress in the AWS console.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab8-8.png)


<div style="page-break-after: always;"></div>

# Lab 9
## AWS Comprehend
In this task, we will leverage AWS Comprehend to analyze text for language detection, sentiment detection, entity detection, key phrase detection and syntax detection.

###  [1]  Client Setup & Language Detection
We'll start by using AWS Comprehend's `detect_dominant_language` method to identify the language in given texts and display the confidence of the prediction.

#### Workflow
1.  **Set Up AWS Comprehend Client**:
    -   Create an AWS Comprehend client using `boto3` with a specific region (`ap-southeast-2` in this case).
2.  **Detect Dominant Language**:
    -   For each piece of text, use `client.detect_dominant_language` to detect the language.
    -   Extract the most probable language from the response.
3.  **Map Language Codes to Language Names**:
    -   Use a dictionary to map language codes (such as `'en'`, `'fr'`, `'es'`, `'it'`) to their corresponding language names (English, French, Spanish, Italian).
4.  **Extract Confidence and Print Results**:
    -   Extract the confidence level in target language and print the language name along with its confidence level.
```
import boto3

# AWS Comprehend client
REGION = "ap-southeast-2"  # Specify the AWS region
client = boto3.client('comprehend', region_name=REGION)

def detect_language(text):
    # Detect the dominant language in the provided text
    response = client.detect_dominant_language(Text=text)
    lang = response['Languages'][0]  # We only use the first detected language

    # Language code for mapping
    language_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'it': 'Italian',
    }

    # Convert results to message
    lang_code = lang['LanguageCode']
    confidence = round(lang['Score'] * 100, 2)
    language_name = language_map.get(lang_code, lang_code)  # Get the language name from the map
    print(f"{language_name} detected with {confidence}% confidence")

# Test with various texts in different languages
texts = [
    "The French Revolution was a period of social and political upheaval in France.",
    "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra.",
    "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits.",
    "L'amor che move il sole e l'altre stelle."
]

# Loop through the texts and detect the language
for text in texts:
    detect_language(text)
```
> #### Code Breakdown
-   **`client = boto3.client('comprehend', region_name=REGION)`**:
    -   Creates an AWS Comprehend client in the specified region (`ap-southeast-2`), allowing us to make requests to the AWS Comprehend service.
-   **`response = client.detect_dominant_language(Text=text)`**:
    -   Calls the `detect_dominant_language` API to detect the dominant language in the provided text.
-   **`lang = response['Languages'][0]`**:
    -   Extracts the first (most confident) language from the list of detected languages.
-   **`language_map = {}`**:
    -   A dictionary that maps language codes to language names. It prints the corresponding language name (e.g., `'en'` -> `'English'`). 
-   **`confidence = round(lang['Score'] * 100, 2)`**:
    -   Extracts the confidence score, convert it to a percentage, and rounds it to two decimal places.

![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-1.png)

###  [2] Sentiment Detection
Sentiment analysis determines if a text expresses positive, negative, neutral, or mixed sentiment.
```
def detect_sentiment(text, language_code='en'):
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = response['Sentiment']
    sentiment_scores = response['SentimentScore']
    
    print(f"Sentiment: {sentiment} with scores: {sentiment_scores}")

# Test sentiment detection with the same texts
for text in texts:
    detect_sentiment(text)
```
> ### Code Breakdown:
1.  **`client.detect_sentiment()`**: Calls AWS Comprehend to detect the sentiment of the input text.
2.  **`response['Sentiment']`**: Extracts the detected sentiment (Positive, Negative, Neutral, or Mixed).
3.  **`response['SentimentScore']`**: Retrieves the confidence scores for each sentiment type.

![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-2.png)

###  [3]  Entity Detection
**Answer**: Entities are some key element or item classes with different types, that helps to identify and classify an object.
```
def detect_entities(text, language_code='en'):
    response = client.detect_entities(Text=text, LanguageCode=language_code)
    entities = response['Entities']
    
    for entity in entities:
        print(f"Entity: {entity['Text']}, Type: {entity['Type']} with {round(entity['Score']*100, 2)}% confidence")


# Test entity detection
for text in texts:
    detect_entities(text)
```
> ### Code Breakdown:
1.  **`client.detect_entities()`**: Detects entities from the input text.
2.  **`response['Entities']`**: Extracts the detected entities and their types.

![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-3.png)

###  [4] Key Phrase Detection
**Answer**: Key phrases are sub-groups of words that are extracted from the whole sentence, which serves as classifiers and provide important concepts to the text.

```
def detect_key_phrases(text, language_code='en'):
    response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    key_phrases = response['KeyPhrases']
    
    for phrase in key_phrases:
        print(f"Key Phrase: {phrase['Text']} with {round(phrase['Score']*100, 2)}% confidence")

# Test key phrase detection
for text in texts:
	detect_key_phrases(text)
```

> ### Code Breakdown:
1.  **`client.detect_key_phrases()`**: Identifies key phrases within the text.
2.  **`response['KeyPhrases']`**: Extracts the list of key phrases detected.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-4.png)

###  [5]  Syntax Detection
**Answer**: Syntax assigns a token to each letter called parts of speech (POS), such as nouns, verbs, adjectives, etc.
```
def detect_syntax(text, language_code='en'):
    response = client.detect_syntax(Text=text, LanguageCode=language_code)
    syntax_tokens = response['SyntaxTokens']
    
    for token in syntax_tokens:
        print(f"Word: {token['Text']}, POS: {token['PartOfSpeech']['Tag']} with {round(token['PartOfSpeech']['Score']*100, 2)}% Confidence")

# Test syntax detection
for text in texts:
	detect_syntax(text)
```
> ### Code Breakdown:

1.  **`client.detect_syntax()`**: Analyzes the text for syntactical elements like nouns, verbs, etc.
2.  **`response['SyntaxTokens']`**: Extracts each word and its corresponding part of speech.

![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-5.png)

## AWS Rekognition
In this task, we will leverage AWS Rekognition to analyze image for **Label Recognition**, **Image Moderation**, **Facial Analysis** and **Text Extraction**.

###  [1]  Setting up instances and Uploading Images
#### Workflow
1.  **Create the Bucket/Rekognition Client**: First, we create an S3 bucket and rekognition client using `boto3` in the region `eu-north-1`. The bucket has a unique bucket name that follows the format `24188516-lab9`
2.  **Upload Images**: After the bucket is created, we upload the four images (`urban.jpg`, `beach.jpg`, `faces.jpg`, `text.jpg`) to this S3 bucket for AWS Rekognition to analyze.
```
import boto3

# Constants
REGION = "ap-southeast-2"
STUDENT_ID = "24188516"
BUCKET_NAME = f"{STUDENT_ID}-lab9"

# Initialize S3 client & Rekognition client
s3 = boto3.client('s3', region_name=REGION)
rekognition = boto3.client('rekognition', region_name=REGION)

# List of images to upload
images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

def upload_images():
    # Create the S3 bucket
    bucket_config = {'LocationConstraint': REGION}
    s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration=bucket_config)

    # Upload images to the bucket
    for image in images:
        s3.upload_file(image, BUCKET_NAME, image)
    print(f"Images uploaded to {BUCKET_NAME}")
```
> ### Code Breakdown:

1.  **`boto3.client()`**: Initializes the client to interact with the AWS S3 service or AWS Rekognition service.
2.  **`create_bucket()`**: Creates an S3 bucket in the specified region, using the student's ID as part of the bucket name.
3.  **`upload_file()`**: Uploads the specified images to the bucket.

These are the files prepared to be uploaded
![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-6.png)

Inspect the S3 bucket interface to verify succesful uploads.
![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-7.png)

### [2] Testing AWS Rekognition for Task Analysis

#### Workflow
1.  **Label Recognition**: Recognize objects, scenes, or actions from the uploaded images.
2.  **Image Moderation**: Check the images for explicit or inappropriate content.
3.  **Facial Analysis**: Analyze facial attributes in the images, such as emotions, gender, and age.
4.  **Text Extraction**: Extract and analyze text from the image containing text.

```
def label_recognition(image):
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': image}},
        MaxLabels=10,
        MinConfidence=70
    )
    print(f"Labels detected in {image}:")
    for label in response['Labels']:
        print(f"  {label['Name']}: {round(label['Confidence'], 2)}% confidence")

def image_moderation(image):
    response = rekognition.detect_moderation_labels(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': image}},
        MinConfidence=70
    )
    print(f"Moderation labels detected in {image}:")
    for label in response['ModerationLabels']:
        print(f"  {label['Name']}: {round(label['Confidence'], 2)}% confidence")

def facial_analysis(image):
    response = rekognition.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': image}},
        Attributes=['ALL']
    )
    print(f"Facial analysis for {image}:")
    for face in response['FaceDetails']:
        print(f"  Age range: {face['AgeRange']['Low']} - {face['AgeRange']['High']}")
        print(f"  Emotions: {', '.join([emotion['Type'] for emotion in face['Emotions'] if emotion['Confidence'] > 50])}")

def text_extraction(image):
    response = rekognition.detect_text(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': image}}
    )
    print(f"Text detected in {image}:")
    for text in response['TextDetections']:
        print(f"  {text['DetectedText']} (Confidence: {round(text['Confidence'], 2)}%)")

# Run the analyses on each image
def run_analyses():
    for image in images:
        label_recognition(image)
        image_moderation(image)
        if image == 'faces.jpg':
            facial_analysis(image)
        if image == 'text.jpg':
            text_extraction(image)

if  __name__  ==  "__main__":
	upload_images()
	run_analyses()
```
> ### Code Breakdown:
1.  **`rekognition.detect_labels()`**:
    -   Detects labels (objects, concepts, and actions) in the image with confidence levels.
   ![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-8.png)
2.  **`rekognition.detect_moderation_labels()`**:
    -   Detects inappropriate content, `Non-explicit Nudity` is detected in `beach.jpg` for example
![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-9.png)
3.  **`rekognition.detect_faces()`**:
    -   Analyzes face details such as age ranges and emotions(run only on `faces.jpg`).
![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-10.png)
4.  **`rekognition.detect_text()`**:
    -   OCR scan and extract text from images that contain written content (run only on `text.jpg`).
![Jupyter Notebook Running](http://127.0.0.1/assets/lab9-11.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTk2MjIxNDY2MywxODY1MjEyMzcxLC0zOD
c5OTgwMzMsMTE5NTY1MTcxMCwtNjEyODUwNDEwLC0yMDYyNDQw
NzQ4LDQwNjUyMTExNywtMTU1MzQxNDgzNywtMTU1MzQxNDgzNy
wyNzQ0MzgxMzksMTY5MTI4MzQ1MywxMDgzMDM1MTEsMTQyOTQ1
MDU3MiwtODUwMjY5NTU4LDY2NjYxNjk2OCwxMTQwMjkwNzU5LD
U2MzY4NDE0MCw1MjA5MTI2NjYsLTEyMjA4OTc4OTksNDg4ODY4
ODgwXX0=
-->