from __future__ import print_function

import json
import boto3
import math
import urllib

print('Loading SiiMii File upload function.')

s3 = boto3.client('s3')
FILE_THRESHOLD = 1024*1000*0.5

def siimii_fileupload(event, context):
    key =urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    bucket = event['Records'][0]['s3']['bucket']['name']
    obj = s3.get_object(Bucket=bucket, Key=key)
    print('file size:' + str(obj["ContentLength"]))
    count = obj["ContentLength"] / FILE_THRESHOLD
    size = math.ceil(count)
    print('create files:' + str(size))
    suffixs = []
    for index in range(0, int(size)):
        if index == size-1:
            suffixs.append(str(index) + '_end')        
        else:
            suffixs.append(str(index))
    if len(suffixs) == 1:
        s3.put_object(Bucket=bucket, Key='photo.jpg.parts._only');
    else:
        for suffix in suffixs:
            s3.put_object(Bucket=bucket, Key='photo.jpg.parts' + suffix);
    return {'result': 'Success'}