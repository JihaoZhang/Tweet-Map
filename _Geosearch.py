import elasticsearch
es = elasticsearch.Elasticsearch()

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
result = es.search(index='t', body=search_body, sort="text:asc")
for hit in result["hits"]["hits"]:
    print hit["_source"]["text"]
    print hit["_source"]["location"]