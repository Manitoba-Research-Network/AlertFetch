from elasticsearch import Elasticsearch


def get_ids(client:Elasticsearch,index:str, query:str)-> set:
    res = client.eql.search(index=index, query=query, fields=[])
    hits = res.raw["hits"]["events"]
    output = set()
    for hit in hits:
        output.add(hit["_id"])
    return output

