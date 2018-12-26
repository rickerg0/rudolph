import boto3, requests
session = boto3.Session(profile_name='default')
rekognition = session.client('rekognition')
#response = requests.get('https://media.alienwarearena.com/media/1327-p.jpg')
response = requests.get('https://www.chicagoautoshow.com/assets/1/7/2018-Super-Car-2.jpg')
response = requests.get('https://b40i4qlau03i7zpg24iid71r-wpengine.netdna-ssl.com/wp-content/uploads/sites/2/2015/12/2015-PIERCE-ENFORCER-E314.jpg')
response_content = response.content
rekognition_response = rekognition.detect_labels(Image={'Bytes': response_content}, MaxLabels=100,MinConfidence=90,)

for label in rekognition_response['Labels']:
    print("{Name} - {Confidence}%".format(**label))
