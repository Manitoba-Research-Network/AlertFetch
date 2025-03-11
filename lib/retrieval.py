import os

from elasticsearch import Elasticsearch
import toml

def get_ids(client:Elasticsearch,index:str, query:str)-> set:
    res = client.eql.search(index=index, query=query, fields=[])
    hits = res.raw["hits"]["events"]
    output = set()
    for hit in hits:
        output.add(hit["_id"])
    return output

def toml_read_query(path:str)->str|None:
    with open(path) as f:
        rule = toml.loads(f.read())

    if "query" not in rule["rule"]:
        return None

    return rule["rule"]["query"]

def dir_toml_read(directory:str, exclude = ("_deprecated", "ml"))-> [str]:
    paths = []
    for root, dirs, files in os.walk(directory):
        # exclude excluded
        excluded = False
        for e in exclude:
            excluded |= root.endswith(e)
        if excluded:
            continue

        # add every absolute path to paths
        paths.extend([root + "/" + f for f in files])
    paths = filter(lambda x: x.endswith(".toml"), paths)
    queries = []
    for path in paths:
        try:
            queries.append(toml_read_query(path))
        except Exception as e:
            print(f"Failed to parse: {path}")
            print(f"\t{e}")
    return queries