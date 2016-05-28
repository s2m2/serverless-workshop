#!/usr/bin/env python

from __future__ import print_function

import os
import urllib
import tempfile

import boto3


MB = (1024*1000)
s3 = boto3.client('s3')

def split_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(
            event['Records'][0]['s3']['object']['key']
            ).decode('utf8')
    split_and_upload(bucket, key)


def split_and_upload(bucket, key, chunksize=int(0.5 * MB)):
    name = "/tmp/%s" % key
    s3.download_file(bucket, key, name)

    tmpdir = tempfile.mkdtemp()
    with open(name, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(chunksize)
            if not chunk: break
            i  = i + 1
            filename = os.path.join(tmpdir, ('part%03d' % i))
            with open(filename, 'wb') as nf:
                nf.write(chunk)
            s3.upload_file(filename, bucket, key + '.part%03d'%i)