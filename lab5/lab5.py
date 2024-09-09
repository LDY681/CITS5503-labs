import boto3 as bt
import os

GroupName = '24188516-sg-lab5'
KeyName = '24188516-key-lab5'
InstanceName1 = '24188516-vm1'
InstanceName2 = '24188516-vm2'
LoadBalancerName = '24188516-elb'
TargetGroupName = '24188516-tg'

# Initialize EC2 and ELBv2 clients
ec2 = bt.client('ec2', region_name='eu-north-1')
elbv2 = bt.client('elbv2')

# 1. Create security group
step1_response = ec2.create_security_group(
    Description="Security group for lab5 environment",
    GroupName=GroupName
)

# 2. Authorize SSH (port 22) and HTTP (port 80) inbound rules
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
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

# 3. Create key-pair
step3_response = ec2.create_key_pair(KeyName=KeyName)
PrivateKey = step3_response['KeyMaterial']
## Save key-pair
with open(f'{KeyName}.pem', 'w') as file:
    file.write(PrivateKey)
## Grant file permission
os.chmod(f'{KeyName}.pem', 0o400)

# 4. Get two of subnets in availability zones
step4_response = ec2.describe_subnets()['Subnets']
Subnets = [subnet['SubnetId'] for subnet in step4_response[:2]]

# 5. Create instances in these two availability zones
Instances = []
for idx, SubnetId in enumerate(Subnets):
    InstanceName = f"24188516-vm{idx + 1}"
    step5_response = ec2.run_instances(
        ImageId='ami-07a0715df72e58928',
        SecurityGroupIds=[step1_response['GroupId']],
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName=KeyName,
        SubnetId=SubnetId
    )
    InstanceId = step5_response['Instances'][0]['InstanceId']
    Instances.append(InstanceId)
    
    # Tag instance with the appropriate name
    ec2.create_tags(
        Resources=[InstanceId],
        Tags=[
            {
                'Key': 'Name',
                'Value': InstanceName
            }
        ]
    )

# 6. Create application load balancer
step6_response = elbv2.create_load_balancer(
    Name=LoadBalancerName,
    Subnets=Subnets,
    SecurityGroups=[step1_response['GroupId']],
    Scheme='internet-facing',
    Type='application'
)
LoadBalancerArn = step6_response['LoadBalancers'][0]['LoadBalancerArn']

# 7. Create target group
VpcId = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
step7_response = elbv2.create_target_group(
    Name=TargetGroupName,
    Protocol='HTTP',
    Port=80,
    VpcId=VpcId,
    TargetType='instance'
)
TargetGroupArn = step7_response['TargetGroups'][0]['TargetGroupArn']

# 8. Register instances as targets
elbv2.register_targets(
    TargetGroupArn=TargetGroupArn,
    Targets=[{'Id': InstanceId} for InstanceId in Instances]
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
print(f"Instance IDs: {Instances}")
print(f"Load Balancer ARN: {LoadBalancerArn}")
print(f"Target Group ARN: {TargetGroupArn}")
