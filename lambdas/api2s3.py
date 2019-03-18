__author__ = 'ronaldbjork'

import boto3
from datetime import datetime
import json

def lambda_handler(event, context):
    is5day = True
    if event is dict:
        date = event['DATETIME']
        is5day = False
    else:
        today = datetime.today()
        month = str(today.month) if today.month > 9 else '0'+ str(today.month)
        day = str(today.day) if today.day > 9 else '0' + str(today.day)
        date = "{}-{}-{}".format(today.year, month, day)
    AWS_BUCKET_NAME = 's3-to-es-bucket'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(AWS_BUCKET_NAME)
    if is5day:
        path = 'logs/Sensordata5day_{}.json'.format(date)
    else:
        path = 'logs/Sensordata_{}.json'.format(date)
    bucket.put_object(
        ACL='public-read',
        ContentType='application/json',
        Key=path,
        Body=json.dumps(event),
    )
    body = {
        "uploaded": "true",
        "bucket": AWS_BUCKET_NAME,
        "path": path,
    }
    return {
        "statusCode": 200,
    }