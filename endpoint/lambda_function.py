from __future__ import print_function

import json
import boto3
import math

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
    size = math.ceil(count)
    print('create files:' + str(size))
    suffixs = []
    for index in range(0, int(size)):
        if index == size-1:
            suffixs.append(str(index) + '_end')        
        else:
            suffixs.append(str(index))
    if len(suffixs) == 1:
        bucket.put_object(Key='photo.jpg.parts.only');
    else:
        for suffix in suffixs:
            bucket.put_object(Key='photo.jpg.parts' + suffix);
    return {'result': 'Success'}