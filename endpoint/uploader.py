#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import boto3
import datetime

__author__ = 'hiroki8080'

bucket_name = 'siimii-compression-upload'
key_name = 'upload_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

argvs = sys.argv
argc = len(argvs)

print argvs
print argc
if(argc != 2):
    print 'Only one can be specified as an argument.'
    quit()

if 'AWS_ACCESS_KEY_ID' not in os.environ or 'AWS_SECRET_ACCESS_KEY' not in os.environ:
    print 'Set the environment variable of AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.'
    quit()

s3 = boto3.resource('s3', aws_access_key_id=os.environ[
                    'AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
s3.Bucket(bucket_name).upload_file(argvs[1], key_name)
