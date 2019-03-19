import boto3
import re
import requests
import json
from requests_aws4auth import AWS4Auth

region = 'us-west-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-s3-es-search-pxnij5i3orrsfd42fgatgtawba.us-west-1.es.amazonaws.com' # the Amazon ES domain, including https://
index = 'lambda-s3-index'
type = 'lambda-type'
url = host + '/' + index + '/' + type

headers = { "Content-Type": "application/json" }

s3 = boto3.client('s3')

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        obj = s3.get_object(Bucket=bucket, Key=key)

        body = obj['Body'].read()
        data = json.loads(str(body, 'utf-8'))
        
        weatherTemperature = data['AT']['av']
        weatherWindDirection = data['WD']['1']['compass_degrees']
        
        timestamp = data['First_UTC']
        date, time = timestamp.split('T')
        year, month, day = date.split('-')
        hour, minute, second = time.split(':')
        
        indexdata = {"DateUTC":date, "TimeUTC":time, "Year":year, "Month":month, "Day":day, "Hour":hour, "Type":"weather", "TempAvg":weatherTemperature, "Wind":weatherWindDirection}
        print(indexdata)
        r = requests.post(url, auth=awsauth, json=indexdata, headers=headers)
    return {"status":str(r.status_code)}



