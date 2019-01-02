from elasticsearch import Elasticsearch, RequestsHttpConnection



def connectES(awsauth,esEndPoint):
 print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
 try:
  esClient = Elasticsearch(
   hosts=[{'host': esEndPoint, 'port': 443}],
   use_ssl=True,
   http_auth=awsauth,
   verify_certs=True,
   connection_class=RequestsHttpConnection)
  return esClient
 except Exception as E:
  print("Unable to connect to {0}".format(esEndPoint))
  print(E)
  exit(3)
  
 

def indexDataElement(esClient,index, type, indexData):
 try:
   esClient.index(index, doc_type=type, body=indexData) 
 except Exception as E:
  print("Unable to Create Index {0}".format(index))
  print(E)
  exit(4)
  
  