try:
    import json
except ImportError:
    import simplejson as json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pprint
import numpy as np
import elasticsearch
import boto3
from watson_developer_cloud import AlchemyLanguageV1
import multiprocessing


session = boto3.Session(
    aws_access_key_id='AKIAJ5IZKUVUKBGNQC5Q',
    aws_secret_access_key='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'
)

es = elasticsearch.Elasticsearch()

if es.indices.exists('t'):
    es.indices.delete('t')
mapping = '''
{
      "mappings": {
         "tweet": {
            "properties": {
                     "location": {
                        "type" : "geo_point"
                  }, "sentiment": {
                        "type" : "string"
                  }
               }
            }
         }
   }
'''
es.indices.create(index='t', ignore=400, body=mapping)

alchemy_language = AlchemyLanguageV1(api_key='c9dae3d9a28f23161fa9f8fbc0e0d08c4f6d1fb0')
sns = boto3.resource('sns', 'us-east-1')
sqs = boto3.resource('sqs', 'us-east-1')
queue = sqs.get_queue_by_name(QueueName='Tweet')
topic = sns.Topic('Tweet')

#pool=multiprocessing.Pool(processes=10)
#rl =pool.map(run, testFL)
while(1):
    for message in queue.receive_messages(MaxNumberOfMessages=1,MessageAttributeNames=['All']):
    #       print message
    #        print message.body
    #        if message.message_attributes is not None:
    #                print message.message_attributes
           txt = message.body
           lat = message.message_attributes.get('Lat').get('StringValue')
           lon = message.message_attributes.get('Lon').get('StringValue')
           ID = message.message_attributes.get('Id').get('StringValue')
           print txt
           print lat
           print lon
           print ID
           senti = alchemy_language.sentiment(text=message.body,language='english')["docSentiment"]["type"]
           d = { 'text': txt,"location" : {"lat" : lat,"lon" : lon},"sentiment":senti}
           es.index(index='t',doc_type='tweet',id=int(ID),body=d)
           topic.publish(
               TopicArn = 'arn:aws:sns:us-east-1:842671666367:Tweet',
               Message=txt,
               MessageStructure='string',
               MessageAttributes={
                    'Lon': {
                        'StringValue': lon,
                        'DataType': 'String'
                    },
                    'Lat': {
                        'StringValue': lat,
                        'DataType': 'String'
                    },
                    'Id': {
                        'StringValue': ID,
                        'DataType': 'String'
                    },
                    'Sentiment': {
                        'StringValue': senti,
                        'DataType': 'String'
                    }
            })
            #message.delete()

