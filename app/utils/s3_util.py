import boto3
import os
from app.utils.logger import logger

# 1. Initialize S3 client and bucket name from environment
s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv("S3_BUCKET")

# 2. Function to upload a file object to S3
def upload_file_to_s3(file_obj, s3_key):
    try:
        # 2.1 Upload the file to S3 at the specified key
        s3_client.upload_fileobj(file_obj, BUCKET_NAME, s3_key)
        logger.info(f"File uploaded to S3 at {s3_key}")
    except Exception as e:
        # 2.2 Log and raise error if upload fails
        logger.error(f"Failed to upload to S3: {str(e)}")
        raise
