import sys
import json
import boto3
import botocore
import datetime
import es
import json
import uuid
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

import urllib

 
def OnDemand(event, context):
    FEATURES_BLACKLIST = ( "BoundingBox" ,"Confidence","Landmarks","Pose","AgeRange","Quality")
    ENDPOINT ='ES endpoint'

    awsauth = AWS4Auth('access', 'secret', 'us-east-1', 'es')
    print(event['Records'])
    esClient= es.connectES(awsauth,ENDPOINT)
   
    session = boto3.Session()
    rekognition = session.client('rekognition')
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('rekognitionTable')

    primaryValue = str(uuid.uuid4())
    dt = str(datetime.datetime.now())
   
    bucket_name =  event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    print("bucket_name "+bucket_name)
    print("filename "+filename)
    
   

    rekognition_response = rekognition.detect_labels(
        Image={"S3Object":
        {"Bucket": bucket_name,
        "Name": filename}}, MaxLabels=100,MinConfidence=90,)
    
    indexLabels = {}
    
    labels = []
    for label in rekognition_response['Labels']:
        labels.append(label['Name'])
        indexLabels[label['Name']]=primaryValue
        
    
    print('labels: '+str(labels)  )
   
   
    if len(labels) > 0:
        response = table.put_item(
            Item={
                'primaryValue': primaryValue,
                'datetime': dt,
                'labels': labels 
            }
        )
        print('indexLabels: '+str(indexLabels)  )
        es.indexDataElement(esClient,'labels', 'image', indexLabels)

    rekognition_response = rekognition.detect_text(Image={"S3Object":
        {"Bucket": bucket_name,
        "Name": filename}}
        )
    print("\n")
   # print(rekognition_response['TextDetections'])
    
    detectedtext = []
    indexText = {}
    for text in rekognition_response['TextDetections']:
        detectedtext.append(text['DetectedText'])
        indexText[text['DetectedText']]=primaryValue

        
    print('Text: '+str(detectedtext)  )
    if len(detectedtext)  > 0:   
        response = table.put_item(
            Item={
                'primaryValue': primaryValue,
                'datetime': dt,
                'detectedtext': detectedtext 
            }   
        )
        print('indexText: '+str(indexText)  )
        es.indexDataElement(esClient,'detectedtext', 'image', indexText)
        
        
    rekognition_response = rekognition.detect_faces(Image={"S3Object":
        {"Bucket": bucket_name,
        "Name": filename}},Attributes=['ALL'])
      
    print('FaceDetails: '+str(rekognition_response)  )
   
    d = rekognition_response['FaceDetails']
    detectedFaces = []
    indexFaces = {}
    for key in d:
        for k,v in key.items():   
            if k not in FEATURES_BLACKLIST:
                if k in 'Emotions':
                    for value in v:
                        if value['Confidence'] > 90.0:
                            detectedFaces.append('Emotions : '+value['Type'])
                            indexFaces[value['Type']]=primaryValue
                            print(value['Type'])
                else:
                    if v['Value'] == True:
                        detectedFaces.append(k+' : '+str(v['Value']))
                        indexFaces[v['Value']]=primaryValue
                        print(k+':'+str(v['Value']))
                    elif  v['Value'] != False:
                        detectedFaces.append(k+' : '+str(v['Value']))
                        indexFaces[value['Value']]=primaryValue
                        print(k+':'+str(v['Value']))
 

    
    print("faces :"+str(detectedFaces)  )
    if len(detectedFaces)  > 0:  
        response = table.put_item(
            Item={
                'primaryValue': primaryValue,
                'datetime': dt,
                'detectedFaces': detectedFaces 
            }
        )  
        print('indexFaces: '+str(indexFaces)  )
        es.indexDataElement(esClient,'faces', 'image', indexFaces)
     
        
    return { "statusCode": 200}    
    
    
    
