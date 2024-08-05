# Lab Report Lab 1

Date: 29/07/2024  
Author: Dayu Liu  

## Lab assignment
**Write a Python script**
Tabulate the un-tabulated response above to have 2 columns with Endpoint and RegionName.

## Steps

### [1] go to the lab directory in linux machine
The python script is located in ~\cits5503\lab1 in the Ubuntu environment
run the following code to land in the right lab directory
`cd ./cits5503/lab1`

## [2] install dependencies
The pandas library is used here to convert un-tabulated data into structured table
run the following code to install the extra dependency
`pip install pandas`

## [3] run the script
run the following code to execute the python script
`python3 lab1.py`

## [4] get the results 
After the script is executed, results are printed in a table structure

| --- | Endpoint | RegionName | OptInStatus |
| --- | --- | --- | --- |
0|       ec2.ap-south-1.amazonaws.com|      ap-south-1|  opt-in-not-required
1|       ec2.eu-north-1.amazonaws.com|      eu-north-1|  opt-in-not-required
2|        ec2.eu-west-3.amazonaws.com|       eu-west-3|  opt-in-not-required
3|        ec2.eu-west-2.amazonaws.com|       eu-west-2|  opt-in-not-required
4|        ec2.eu-west-1.amazonaws.com|       eu-west-1|  opt-in-not-required
5|   ec2.ap-northeast-3.amazonaws.com|  ap-northeast-3|  opt-in-not-required
6|   ec2.ap-northeast-2.amazonaws.com|  ap-northeast-2|  opt-in-not-required
7|   ec2.ap-northeast-1.amazonaws.com|  ap-northeast-1|  opt-in-not-required
8|     ec2.ca-central-1.amazonaws.com|    ca-central-1|  opt-in-not-required
9|        ec2.sa-east-1.amazonaws.com|       sa-east-1|  opt-in-not-required
10|  ec2.ap-southeast-1.amazonaws.com|  ap-southeast-1|  opt-in-not-required
11|  ec2.ap-southeast-2.amazonaws.com|  ap-southeast-2|  opt-in-not-required
12|    ec2.eu-central-1.amazonaws.com|    eu-central-1|  opt-in-not-required
13|       ec2.us-east-1.amazonaws.com|       us-east-1|  opt-in-not-required
14|       ec2.us-east-2.amazonaws.com|       us-east-2|  opt-in-not-required
15|       ec2.us-west-1.amazonaws.com|       us-west-1|  opt-in-not-required
16|       ec2.us-west-2.amazonaws.com|       us-west-2|  opt-in-not-required

