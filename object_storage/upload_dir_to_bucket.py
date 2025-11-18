import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = 'ncp_iam_BPA*****'
secret_key = 'ncp_iam_BPK*****'

bucket_name = "seong-contents-bucket"
local_dir  = "./upload_test2" # 업로드할 로컬디렉토리 지정

def main():
    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key, config=Config(signature_version="s3v4", s3={"addressing_style":"path"},
            request_checksum_calculation="when_required", response_checksum_validation="when_required"))

    for root, _, files in os.walk(local_dir):
        for fname in files:
            local_file_path = os.path.join(root, fname)
            rel_path = os.path.relpath(local_file_path, local_dir)
            object_name = rel_path.replace("\\", "/")
            try:
                s3.upload_file(local_file_path, bucket_name, object_name)
                print(f"[성공] {local_file_path} → s3://{bucket_name}/{object_name}")
                print("-" * 40)
                print("업로드가 완료되었습니다.")
            except ClientError as e:
                print("-" * 40)
                print("업로드 실패:", e.response)

if __name__ == "__main__":
    main()
