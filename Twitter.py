try:
    import json
except ImportError:
    import simplejson as json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pprint
import numpy as np
import boto3


#consumer key, consumer secret, access token, access secret.
ACCESS_TOKEN = '3837655757-UJd7ZXp2LbLRlyjWVLGXmZNlCRh9c9dIEniikEf'
ACCESS_SECRET = 'NMHUbHMKWK5E5Cjzl3KpjGpn013zaJoOJpYD1DXFwVMI8'
CONSUMER_KEY = 'o3AmLlX5kiQaiIDdSTaqwUEt7'
CONSUMER_SECRET = 'xOO0Lf2IQgeH4ez5MeDU7TZ6UNk49BoLu8a9PBk4jt50YzMrPZ'

session = boto3.Session(
    aws_access_key_id='AKIAJ5IZKUVUKBGNQC5Q',
    aws_secret_access_key='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'
)
sns = boto3.resource('sns', 'us-east-1')
sqs = boto3.resource('sqs', 'us-east-1')
queue = sqs.get_queue_by_name(QueueName='Tweet')
topic = sns.Topic('Tweet')

class listener(StreamListener):
    def __init__(self):
        self.count = 0
    def on_data(self, data):
        if data is not None:
            jsond = json.loads(data)
            if jsond.get('geo') is not None:
                print 1
                coor = jsond.get('geo').get('coordinates')
                lat = str(coor[0])
                lon = str(coor[1])
                txt = jsond.get('text')
                queue.send_message(MessageBody=txt, MessageAttributes={
                    'Lon': {
                        'StringValue': lon,
                        'DataType': 'String'
                    },
                    'Lat': {
                        'StringValue': lat,
                        'DataType': 'String'
                    },
                    'Id': {
                        'StringValue': str(self.count),
                        'DataType': 'String'
                    }
                })
                
                if self.count == 199:
                    self.count = 0
                else:
                    self.count +=1
                print self.count
            #pp.pprint (jsond)
        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["love","happy","play", "sleep", "eat", "work", "music", "food", "trump", "clinton"])
