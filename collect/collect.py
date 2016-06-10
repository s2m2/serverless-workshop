# -*- coding: utf-8 -*-
from  __future__ import print_function                                                                                                                                                                                                        

import json
import urllib
import boto3
import zipfile
import time

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # File Name Format.
    # 1.only
    # yoropiku.photo.jpg.parts._only.zip
    # 2.multi
    # yoropiku.photo.jpg.parts.0.zip
    # yoropiku.photo.jpg.parts.1.zip
    # yoropiku.photo.jpg.parts.2_end.zip
    
    targets = []
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    keys = key.split('.')
    index = keys[len(keys)-2].split('_')[0]
    prefix = '.'.join([keys[0],keys[1],keys[2],keys[3]])
    
    list = get_list(bucket, prefix, index)
    if list is None:
        return True
    
    for target in list['Contents']:
        tmp_name = create_tmp(bucket, target['Key'])
        print(tmp_name)
        targets.append(tmp_name)
    
    zip_name = '/tmp/compact.zip'
    with zipfile.ZipFile(zip_name, 'w') as f:
        for zip_target in targets:
            f.write(zip_target)
    s3.upload_file(zip_name, bucket, 'compact.zip')

def create_tmp(bucket, key):
    tmp_file = "/tmp/{}".format(key)
    s3.download_file(bucket, key, tmp_file)
    return tmp_file

def get_list(bucket, prefix, index):
    list = s3.list_objects(Bucket=bucket, Prefix=prefix)
    if len(list['Contents']) < int(index) + 1:
        time.sleep(10) # Retry after 10 seconds.
        list = s3.list_objects(Bucket=bucket, Prefix=prefix)
        if len(list['Contents']) < int(index) + 1:
            s3.put_object(Key='error', Bucket=bucket);
        list = None
    return list

    