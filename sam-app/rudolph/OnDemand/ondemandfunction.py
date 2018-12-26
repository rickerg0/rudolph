import sys
import json
import boto3
import botocore
       
def OnDemand(event, context):
   
    print(event['Records'])
  
    s3Client= boto3.client('s3')
  
    bucket_name =  event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    print("bucket_name "+bucket_name)
    print("filename "+filename)
    
    obj = s3Client.get_object(Bucket=bucket_name, Key=filename)
     # get lines inside the csv
    data = obj['Body'].read()
    #print (data)
    #theData = json.loads(data)
    #print(theData)
   
        
            
    return { "statusCode": 200}
    
