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


### Set Up a Virtual Environment

To create a new isolated Python environment, run the following command:

```bash
python3 -m venv myvenv
```

#### Key Parameters:

-   **`-m venv`**: Uses the `venv` module to create a new virtual environment.
-   **`myvenv`**: Specifies the name of the directory to store the virtual environment. You can replace `myvenv` with any directory name of your choice.

This command will create a new directory called `myvenv` containing the Python interpreter, standard library, and other resources, allowing you to manage dependencies separately from the global Python environment.

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

Once the commands are executed, Django creates the following structure for your project:

- **`lab/`**: The project directory containing the settings and configurations for the entire Django project.
  - **`__init__.py`**: Marks the directory as a Python package.
  - **`settings.py`**: Contains project settings such as installed apps, middleware, and database configurations.
  - **`urls.py`**: The project's URL declarations for routing HTTP requests.
  - **`wsgi.py`**: The entry point for WSGI-compatible web servers to serve your project.
  - **`asgi.py`**: The entry point for ASGI-compatible servers for asynchronous support.
- **`manage.py`**: A command-line utility to interact with the Django project (e.g., running the server, creating migrations).

- **`polls/`**: The app directory that houses the `polls` app created using `startapp`.
  - **`migrations/`**: Directory for database migrations files.
  - **`admin.py`**: For registering models with the Django admin.
  - **`apps.py`**: Configuration for the app itself.
  - **`models.py`**: Where database models are defined.
  - **`tests.py`**: Houses unit tests for the app.
  - **`views.py`**: Where request-handling functions and classes are defined.

The files and structure created by Django provide a foundation for organizing and developing the project. As we progress, we will work on these files to build the application and understand their specific roles and functionalities.


### [6] Install Nginx

To install the Nginx web server, run the following command:

```bash
apt install nginx
```
#### Key Parameters:
-   **`install nginx`**: Downloads and installs the `nginx` package from the repository, including all necessary dependencies.

This command sets up the Nginx web server, which can be used as a reverse proxy, load balancer, or HTTP cache for your applications.
![enter image description here](http://127.0.0.1/assets/lab6-8.png)

### [7] Configure nginx

To configure Nginx to work as a reverse proxy for your Django application, go to the Nginx configuration file located at `/etc/nginx/sites-enabled/default` and add the following.

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

- **`listen`**: Specifies the port Nginx listens on. Here, **80** is the default HTTP port for web traffic. The second `listen` line is for IPv6.
  
- **`proxy_set_header X-Forwarded-Host $host;`**: Sets the `X-Forwarded-Host` header to the host of the original request. This header preserves the original `Host` header sent by the client.

- **`proxy_set_header X-Real-IP $remote_addr;`**: Sets the `X-Real-IP` header to the real client IP address. This header helps in passing the original client's IP address to the proxied server.

- **`proxy_pass http://127.0.0.1:8000;`**: Forwards incoming traffic to `http://127.0.0.1:8000`, where your Django application is running. This allows Nginx to act as a reverse proxy, handling requests and passing them to your Django server.

This configuration ensures that all incoming traffic to your server's port **80** is passed to the Django app running locally on port **8000**.

### [8] Restart nginx
To apply our new configuration, we need to restart the Nginx service, run the following command:
```
service nginx restart
```
#### Key Parameters:

-   **`service`**: Manages system services.
-   **`nginx`**: Specifies the Nginx service to be managed.
-   **`restart`**: Restarts the Nginx service, stopping it if running and then starting it again to apply any configuration changes.

This command ensures that any updates or changes made to the Nginx configuration are applied.

### [9] Access your EC2 instance

In the app directory `/opt/wwc/mysites/lab`, run the following command to start your Django application server on port **8000**:

```
python3 manage.py runserver 8000
```
#### Key Parameters:

-   **`runserver`**: Starts the Django development server.
-   **`8000`**: Specifies the port on which the server will listen for requests. In this case, it's **8000**.

We can now access the web app via `http://13.61.7.212:8000`.
![enter image description here](http://127.0.0.1/assets/lab6-9.png)

## Set up Django inside the created EC2 instance

### [1] Edit the following files (create them if not exist)

In `polls/views.py`, create a view that returns a simple HTTP response "Hello World":
```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```
-   **`HttpResponse`**: A Django class that returns a simple HTTP response containing the string `"Hello, world."`.

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

### [2] Run the web server again
Now we can apply the changes and restart the server to see the changes.
```
python3 manage.py runserver 8000
```


### [3] Access the EC2 instance

Access the polls index page with `Hello,World` message by visiting `http://13.61.7.212/polls/`. Access the built-in admin module by visiting `http://13.61.7.212/admin/`
![enter image description here](http://127.0.0.1/assets/lab6-10.png)

![enter image description here](http://127.0.0.1/assets/lab6-11.png)

## Set up an ALB

### [1] Create an application load balancer & Health Check
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
### Code Explanation

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

### [3] Access
Get the ALB DNS url from `print(f"Load Balancer DNS Name: {LoadBalancerDnsName}")`,  now access its url with path `/polls/` to see health check results: http://24188516-elb-920225157.eu-north-1.elb.amazonaws.com/polls/
![enter image description here](http://127.0.0.1/assets/lab6-12.png)

**NOTE**: When you are done, delete the instance and ALB you created.
<div style="page-break-after: always;"></div>

# Lab 7

<div style="page-break-after: always;"></div>

# Lab 8

<div style="page-break-after: always;"></div>

# Lab 9

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIxMTY1NzkzMTksMTU5MDcwODA5LC0xNT
QwMzY2Mzg2LC0xMDk4MzY5NDY5LC0xNDMyOTAzMTA4LC0zNzQy
OTM2NjcsLTE3Njg3NTY4MzMsLTE5NDI1NDEyNzcsMTg1MTk2ND
Q4OCwtMTY3NTgzOTc3NSwtMTgyNzQyODQ3NSwtMTc3MDk2NzY0
MywxODczOTAzMjQ1LDE5MjY5MTQyNDgsMTkyNjkxNDI0OCwxOT
EyMjE3Mzg3LC03NDUxMjE3NDIsMTAxOTA2ODUxMCwxMDQ0ODI0
MjI1LDEwMjM5NTUwN119
-->