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