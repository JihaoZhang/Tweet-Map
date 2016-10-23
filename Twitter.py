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

pp = pprint.PrettyPrinter(indent=4)
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
                  }
               }
            }
         }
   }
'''
es.indices.create(index='t', ignore=400, body=mapping)

#consumer key, consumer secret, access token, access secret.
ACCESS_TOKEN = '3837655757-UJd7ZXp2LbLRlyjWVLGXmZNlCRh9c9dIEniikEf'
ACCESS_SECRET = 'NMHUbHMKWK5E5Cjzl3KpjGpn013zaJoOJpYD1DXFwVMI8'
CONSUMER_KEY = 'o3AmLlX5kiQaiIDdSTaqwUEt7'
CONSUMER_SECRET = 'xOO0Lf2IQgeH4ez5MeDU7TZ6UNk49BoLu8a9PBk4jt50YzMrPZ'

class listener(StreamListener):
    def __init__(self):
        self.count = 0
    def on_data(self, data):
        if data is not None:
            print 1
            jsond = json.loads(data)
            if jsond.get('geo') is not None:
                coor = jsond.get('geo').get('coordinates')
                lat = coor[0]
                lon = coor[1]
                d = { 'text': jsond.get('text'),"location" : {"lat" : lat,"lon" : lon}}
                es.index(index='t',doc_type='tweet',id=self.count,body=d)
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
#twitterStream.filter(track=["love","car"])