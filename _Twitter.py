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
            jsond = json.loads(data)
            if jsond.get('place') is not None:
                coor = np.array(jsond.get('place').get('bounding_box').get('coordinates'))
                m = coor.mean(1).tolist()
                d = { 'text': jsond.get('text'),'coor': m}
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
# twitterStream.filter(track=["love"])
twitterStream.filter(track=["love","happy","play", "sleep", "eat", "work", "china", "america", "trump", "clinton"])