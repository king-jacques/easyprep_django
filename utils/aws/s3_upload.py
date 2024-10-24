import boto3
from django.conf import settings
from botocore.exceptions import NoCredentialsError
import os
# Create an S3 client using your AWS credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)


def upload_images_to_s3(folder_path, bucket_name='easyprepassets'):
    """Upload all images from a local folder to S3 and print URLs."""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            image_name = f'{filename}'  # S3 path where file will be uploaded
            
            try:
                # Upload the file
                s3_client.upload_file(
                    file_path, 
                    bucket_name, 
                    image_name,
                    ExtraArgs={'ContentType': 'image/jpeg'}  # or 'image/png' based on file type
                )

                # Generate and print the S3 public URL
                s3_url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
                print(f"Uploaded: {filename} -> {s3_url}")
            
            except FileNotFoundError:
                print(f"File {file_path} not found.")
            except NoCredentialsError:
                print("AWS credentials not available.")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")


def view_bucket(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        print(f'Contents of bucket "{bucket_name}":')
        for obj in response['Contents']:
            print(f' - {obj["Key"]}')
    else:
        print(f'The bucket "{bucket_name}" is empty.')


def delete_bucket_object(bucket_name, obj_name):
    response = s3_client.delete_object(Bucket=bucket_name, Key=obj_name)