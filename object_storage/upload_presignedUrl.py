import os
import sys
import boto3
import requests
from botocore.config import Config
from botocore.exceptions import NoCredentialsError, ClientError

endpoint_url = "https://kr.object.ncloudstorage.com"
region_name  = "kr-standard"

access_key = "ncp_iam_BPA*****"
secret_key = "ncp_iam_BPK*****"

bucket_name = "seong-contents-bucket"
local_dir  = "./upload_test" # 업로드할 로컬디렉토리 지정

def upload_file(s3, local_path, object_key):
    try:
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,
            HttpMethod="PUT"
        )
        with open(local_path, "rb") as f:
            resp = requests.put(url, data=f)
            if resp.status_code == 200:
                print(f"[성공] {local_path} → s3://{bucket_name}/{object_key}")
                print("-" * 40)
                print("업로드가 완료되었습니다.")
            else:
                print(f"[실패] {local_path} 업로드 중 오류 발생:", resp.status_code, resp.text)
    except ClientError as e:
        print(f"에러 발생: {e}")

def main():
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4", s3={"addressing_style":"path"})
    )

    for root, _, files in os.walk(local_dir):
        for fname in files:
            local_path = os.path.join(root, fname)
            rel_path = os.path.relpath(local_path, local_dir)
            object_key = rel_path.replace("\\", "/")
            upload_file(s3, local_path, object_key)

if __name__ == "__main__":
    main()
