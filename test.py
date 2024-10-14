# Install libraries
# Install SageMaker via jupyter notebook
!pip install sagemaker
# Install pandas and numpy jupyter notebook
!pip install pandas
!pip install numpy

# Prepare a SageMaker session
import sagemaker
import boto3

import numpy as np  # For matrix operations and numerical processing
import pandas as pd  # For munging tabular data
from time import gmtime, strftime
import os

smclient = boto3.Session().client("sagemaker")
iam = boto3.client('iam')
sagemaker_role = iam.get_role(RoleName='SageMakerRole')['Role']['Arn']
region = 'eu-north-1' # use the region you are mapped to 
student_id = "24188516" # use your student id 
bucket = '24188516-lab8' # use <studentid-lab8> as your bucket name
prefix = f"sagemaker/{student_id}-hpo-xgboost-dm" 
# Create an S3 bucket using the bucket variable above. The bucket creation is done using the region variable above.
# Create an object into the bucket. The object is a folder and its name is the prefix variable above. 
s3 = boto3.client('s3', region_name=region)
s3.create_bucket(Bucket=bucket) # create the bucket in our region
s3.put_object(Bucket=bucket, Key=f"{prefix}/") # create a folder object with the prefix

# Download a dataset
# Read and download the marketing dataset from UCI's ML Repository [here](https://archive.ics.uci.edu/ml/datasets/bank+marketing).
# NOTE: You can download and unzip the dataset using the commands below.
!wget -N https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip
!unzip -o bank-additional.zip

# Read the dataset into a Pandas data frame and answer the following two questions:
#1. Which variables in the dataset are categorical? Give at least four variables.
#2. Which variables in the dataset are numerical? Give at least four variables.
data = pd.read_csv("./bank-additional/bank-additional-full.csv", sep=";")
pd.set_option("display.max_columns", 500)  # Make sure we can see all of the columns
pd.set_option("display.max_rows", 50)  # Keep the output on one page
data

# Process the data by adding two new indicator columns and then expands categorical columns into binary dummy columns for modelling purposes.
data["no_previous_contact"] = np.where(
    data["pdays"] == 999, 1, 0
)  # Indicator variable to capture when pdays takes a value of 999
data["not_working"] = np.where(
    np.in1d(data["job"], ["student", "retired", "unemployed"]), 1, 0
)  # Indicator for individuals not actively employed
model_data = pd.get_dummies(data)  # Convert categorical variables to sets of indicators
model_data

# Remove the economic features and duration from our data as they would need to be forecasted with high precision to use as inputs in future predictions.   
model_data = model_data.drop(
    ["duration", "emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"],
    axis=1,
)
model_data

# Split the data into training, validation and test
# We split the dataset into training (70%), validation (20%), and test (10%) datasets and convert the datasets to an appropriate format. We will use the training and validation datasets during training. Test dataset will be used to evaluate model performance after it is deployed to an endpoint.
# Amazon SageMaker's XGBoost algorithm expects data in the libSVM or CSV data format. In this lab, we use the CSV format. Note that the first column must be the target variable and the CSV should not include headers. Also, notice that although repetitive it’s easier to do this after the train|validation|test split rather than before. This avoids any misalignment issues due to random reordering.
train_data, validation_data, test_data = np.split(
    model_data.sample(frac=1, random_state=1729),
    [int(0.7 * len(model_data)), int(0.9 * len(model_data))],
)

pd.concat([train_data["y_yes"], train_data.drop(["y_no", "y_yes"], axis=1)], axis=1).to_csv(
    "train.csv", index=False, header=False
)
pd.concat(
    [validation_data["y_yes"], validation_data.drop(["y_no", "y_yes"], axis=1)], axis=1
).to_csv("validation.csv", index=False, header=False)
pd.concat([test_data["y_yes"], test_data.drop(["y_no", "y_yes"], axis=1)], axis=1).to_csv(
    "test.csv", index=False, header=False
)

#Copy the file to the S3 bucket created earlier for Amazon SageMaker training to pick up.
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "train/train.csv")
).upload_file("train.csv")
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "validation/validation.csv")
).upload_file("validation.csv")

# Setup hyperparameter tuning
# Set up the the name and configuration for a hyperparameter tuning job.
from time import gmtime, strftime, sleep

# Names have to be unique. You will get an error if you reuse the same name
tuning_job_name = f"{student_id}-xgboost-tuningjob-01"

print(tuning_job_name)

tuning_job_config = {
    "ParameterRanges": {
        "CategoricalParameterRanges": [],
        "ContinuousParameterRanges": [
            {
                "MaxValue": "1",
                "MinValue": "0",
                "Name": "eta",
            },
            {
                "MaxValue": "10",
                "MinValue": "1",
                "Name": "min_child_weight",
            },
            {
                "MaxValue": "2",
                "MinValue": "0",
                "Name": "alpha",
            },
        ],
        "IntegerParameterRanges": [
            {
                "MaxValue": "10",
                "MinValue": "1",
                "Name": "max_depth",
            }
        ],
    },
    "ResourceLimits": {"MaxNumberOfTrainingJobs": 2, "MaxParallelTrainingJobs": 2},
    "Strategy": "Bayesian",
    "HyperParameterTuningJobObjective": {"MetricName": "validation:auc", "Type": "Maximize"},
}

# Specify the XGBoost algorithm for subsequent tuning.
from sagemaker.image_uris import retrieve
# Use XGBoost algorithm for training
training_image = retrieve(framework="xgboost", region=region, version="latest")

s3_input_train = "s3://{}/{}/train".format(bucket, prefix)
s3_input_validation = "s3://{}/{}/validation/".format(bucket, prefix)

training_job_definition = {
    "AlgorithmSpecification": {"TrainingImage": training_image, "TrainingInputMode": "File"},
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "CompressionType": "None",
            "ContentType": "csv",
            "DataSource": {
                "S3DataSource": {
                    "S3DataDistributionType": "FullyReplicated",
                    "S3DataType": "S3Prefix",
                    "S3Uri": s3_input_train,
                }
            },
        },
        {
            "ChannelName": "validation",
            "CompressionType": "None",
            "ContentType": "csv",
            "DataSource": {
                "S3DataSource": {
                    "S3DataDistributionType": "FullyReplicated",
                    "S3DataType": "S3Prefix",
                    "S3Uri": s3_input_validation,
                }
            },
        },
    ],
    "OutputDataConfig": {"S3OutputPath": "s3://{}/{}/output".format(bucket, prefix)},
    "ResourceConfig": {"InstanceCount": 1, "InstanceType": "ml.m5.xlarge", "VolumeSizeInGB": 10},
    "RoleArn": sagemaker_role,
    "StaticHyperParameters": {
        "eval_metric": "auc",
        "num_round": "1",
        "objective": "binary:logistic",
        "rate_drop": "0.3",
        "tweedie_variance_power": "1.4",
    },
    "StoppingCondition": {"MaxRuntimeInSeconds": 43200},
}

# Launch the tuning job.
#Launch Hyperparameter Tuning Job
smclient.create_hyper_parameter_tuning_job(
    HyperParameterTuningJobName=tuning_job_name,
    HyperParameterTuningJobConfig=tuning_job_config,
    TrainingJobDefinition=training_job_definition,
)

# Go to AWS console (SageMaker-> Training -> Hyperparameter tuning jobs) to monitor the progress of the hyperparameter tuning job ([How to monitor the progress of a job?](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-monitor.html)).
# The tuning will normally take between 2-4 minutes. Make ensure that the tuning job is completed successfully from the console. Also check the job output inside the s3 object you created. Last, remove all the AWS resources you used in this lab.
# NOTE: if the tuning job fails, check if you meet this error, ClientError: Non-numeric value 'F' found in the header line 'False,54,3,999,0,1,0,False,False,False,False,False...' of the file 'train.csv'. If so, you should convert the non-numeric values to numeric ones (i.e., True/False to 1/0). After that, rename your tuning job in the provided code and run it again.