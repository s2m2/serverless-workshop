# -*- coding: utf-8 -*-
from  __future__ import print_function                                                                                                                                                                                                        

import json
import urllib
import boto3
import zipfile

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        print("bucket:{}".format(bucket))
        compress(bucket, key)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

def compress(bucket, key):
    tmp_file = "/tmp/" + key
    zip_file = key + ".zip"
    tmp_zip_file = "/tmp/" + zip_file
    print(tmp_file)
    print(zip_file)
    s3.download_file(bucket, key, tmp_file)
    print("downloaded")
    with zipfile.ZipFile(tmp_zip_file, 'w') as f:
        f.write(tmp_file)
    s3.upload_file(tmp_zip_file, bucket, zip_file)
