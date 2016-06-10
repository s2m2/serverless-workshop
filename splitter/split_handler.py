#!/usr/bin/env python


from __future__ import print_function

import os
import urllib
import tempfile

import boto3


MB = (1024*1000)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(
            event['Records'][0]['s3']['object']['key']
            ).decode('utf8')
    split_and_upload(bucket, key)

def split_and_upload(bucket, key, chunksize=int(0.5 * MB)):
    name, part_number = get_fileinfo(key)
    tmpname = "/tmp/%s" % name
    s3.download_file(bucket, name, tmpname)

    tmpdir = tempfile.mkdtemp()
    with open(tmpname, 'rb') as f:
        f.seek((part_number-1) * chunksize)
        chunk = f.read(chunksize)
        filename = os.path.join(tmpdir, key)
        with open(filename, 'wb') as nf:
            nf.write(chunk)
        s3.upload_file(filename, bucket, "yoropikune." + key)

def get_fileinfo(filename):
    name, part = filename.rsplit(".", 1)
    part_number = part.strip("parts")
    if not part_number:
        sys.exit("filename error")
    if "end" in part_number:
        part_number = int(part_number.rstrip("_end"))
    elif "only" in part_number:
        part_number = 1
    else:
        sys.exit("filename error")
    return  name, int(part_number)
