from elasticsearch import Elasticsearch
import toml

def get_ids(client:Elasticsearch,index:str, query:str)-> set:
    res = client.eql.search(index=index, query=query, fields=[])
    hits = res.raw["hits"]["events"]
    output = set()
    for hit in hits:
        output.add(hit["_id"])
    return output

def toml_read_query(path:str):
    with open(path) as f:
        rule = toml.loads(f.read())

    if "query" not in rule["rule"]:
        return None

    return rule["rule"]["query"]
