#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import boto3

__author__ = 'hiroki8080'

bucket_name = 'siimii-compression'
key_name = 'file_upload'

argvs = sys.argv
argc = len(argvs)

if(argc != 1):
    print 'Only one can be specified as an argument.'
    quit()

if 'AWS_ACCESS_KEY_ID' not in os.environ  or 'AWS_SECRET_ACCESS_KEY' not in os.environ:
        print 'Set the environment variable of AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.'
        quit()

conn = S3Connection(os.envirion['AWS_ACCESS_KEY_ID'], os.envirion['AWS_SECRET_ACCESS_KEY'])
bucket = conn.create_bucket(bucket_name)

k = Key(bucket)

k.key = key_name
k.set_conetns_from_filename(argvs[0])

