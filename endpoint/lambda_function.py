from __future__ import print_function

import json
#import boto3

AWS_S3_BUCKET_NAME = ''

print('Loading SiiMii File upload function.')

def siimii_fileupload(event, context):
#        s3 = boto3.resource('s3')
#        bucket = s3.Bucket(AWS_S3_BUCKET_NAME)
    if event['file']:
        print(event['file'])
        return { 'result':'Success' } 
    else:
        return { 'result':'File has not been set.'}