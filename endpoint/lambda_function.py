from __future__ import print_function

import json
import boto3

AWS_S3_BUCKET_NAME = 'siimii-compression-upload'

FILE_THRESHOLD = 1024*1000*0.5

print('Loading SiiMii File upload function.')


def siimii_fileupload(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    s3 = boto3.resource('s3')
    client = boto3.client('lambda')
    bucket = s3.Bucket(AWS_S3_BUCKET_NAME)
    obj = bucket.Object(file_name)
    print('file size:' + str(obj.content_length))
    count = obj.content_length / FILE_THRESHOLD
    print('create files:' + str(count))
    for var in range(0, count):
        bucket.put_object(Key='photo.jpg.parts' + str(var));
    return {'result': 'Success'}
