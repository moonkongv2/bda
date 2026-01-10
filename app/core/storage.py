import os
import shutil
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from app.core import config

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )

def save_file(file: UploadFile, filename: str) -> str:
    """
    Save file to local storage or S3 based on configuration.
    Returns the file path or S3 key.
    """
    if config.STORAGE_TYPE == "s3":
        return _save_to_s3(file, filename)
    else:
        return _save_to_local(file, filename)

def _save_to_local(file: UploadFile, filename: str) -> str:
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, filename)

    # Reset file pointer to beginning
    file.file.seek(0)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_location

def _save_to_s3(file: UploadFile, filename: str) -> str:
    s3_client = get_s3_client()
    try:
        file.file.seek(0)
        s3_client.upload_fileobj(
            file.file,
            config.S3_BUCKET_NAME,
            filename
        )
        return f"s3://{config.S3_BUCKET_NAME}/{filename}"
    except NoCredentialsError:
        raise Exception("AWS Credentials not found")
    except Exception as e:
        raise Exception(f"Failed to upload to S3: {str(e)}")
