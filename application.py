from flask import Flask, render_template, redirect, abort, url_for
from flask import request
from elasticsearch import Elasticsearch, exceptions
import json

application = Flask(__name__)

es = Elasticsearch()
keywords = ["love","happy","play", "sleep", "eat", "work", "music", "food", "trump", "clinton"]

@application.route('/')
def showGoogleMap():
    query = request.args.get('q', '')
    print query
    res = es.search(index='t', doc_type='tweet', body={
      "query": {"query_string": {"query": query}},
      "size": 750})
    coords, results = [], []
    if res["hits"]["hits"]:
      coords = [{"lat": r["_source"]["location"]["lat"], "lng": r["_source"]["location"]["lon"]} for r in res["hits"]["hits"]]
      results = [r["_source"]["text"] for r in res["hits"]["hits"]]
    coordsJSON = json.dumps(coords).replace('\"','')
    return render_template("googlemap.html",
                           coords=coordsJSON,
                           keywords=keywords,
                           query=query,
                           results=results)

@application.route('/distance')
def distance_filter():
    query = request.args.get('q', '')
    search_body = {
        "filter" : {
            "geo_distance" : {
                "distance" : "2300km",
                "location" : {
                    "lat" : 15,
                    "lon" : 100
                }
            }
        }
    }
    res = es.search(index='t', doc_type='tweet', body=search_body, sort="text:asc")
    coords, results = [], []
    if res["hits"]["hits"]:
      coords = [{"lat": r["_source"]["location"]["lat"], "lng": r["_source"]["location"]["lon"]} for r in res["hits"]["hits"]]
      results = [r["_source"]["text"] for r in res["hits"]["hits"]]
    coordsJSON = json.dumps(coords).replace('\"','')
    return render_template("googlemap.html",
                           coords=coordsJSON,
                           keywords=keywords,
                           query=query,
                           results=results)


@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@application.errorhandler(404)
def page_not_found(error):
    return 'Oh. Nothing is here.'

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
