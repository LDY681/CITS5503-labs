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
Subnets = [subnet['SubnetId'] for subnet in subnet_response[:2]]
print(subnet_response, Subnets)