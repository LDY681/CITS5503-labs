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

if __name__ == "__main__":
    upload_images()
    run_analyses()
