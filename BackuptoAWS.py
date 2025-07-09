import boto3

def upload_to_s3(local_file, bucket_name, s3_filename):
    s3 = boto3.client('s3',
                      aws_access_key_id="YOUR_ACCESS_KEY",
                      aws_secret_access_key="YOUR_SECRET_KEY")
    
    try:
        s3.upload_file(local_file, bucket_name, s3_filename)
        print("Uploaded to S3:", s3_filename)
    except Exception as e:
        print("S3 Upload Error:", e)
