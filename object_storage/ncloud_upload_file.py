import boto3
import logging
logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = 'ncp_iam_BPA*****'
secret_key = 'ncp_iam_BPK*****'

if __name__ == "__main__":
    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    bucket_name = 'seong-contents-bucket'

    # create folder
    object_name = 'sdk_test.txt'

    s3.put_object(Bucket=bucket_name, Key=object_name)

    # upload file
    object_name = 'sdk_test.txt'
    local_file_path = './upload_test/sdk_test.txt'

    s3.upload_file(local_file_path, bucket_name, object_name)
