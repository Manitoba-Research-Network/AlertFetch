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

def toml_read_query(path:str)->dict|None:
    with open(path) as f:
        rule = toml.loads(f.read())["rule"]

    if "query" not in rule or "language" not in rule:
        return None

    out = {"query": rule["query"], "lang":rule["language"]}
    return out

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
            rule = toml_read_query(path)
            if rule is None: # skip null rules
                continue
            queries.append({"rule":rule, "path":path})
        except Exception as e:
            print(f"Failed to parse: {path}")
            print(f"\t{e}")
    return queries

def get_events(client:Elasticsearch, index:str, query:str) -> dict:#todo this needs to handle paginated results
    res = client.eql.search(index=index, query=query, fields=[], size=10000)
    try:
        hits = res.raw["hits"]["events"]
    except KeyError:
        hits = res.raw["hits"]["sequences"]
    output = {}
    for hit in hits:
        output[hit["_id"]] = {**hit, "IPG5_source":query}
    #if len(hits) == 0:
    #    print(query)
    #    print("\n")
    return output

def get_inverse_ids(client:Elasticsearch,  index:str, ids:list):
    q = f"any where event.id not in ({_list_to_string(ids)})"
    print(f"Executing {q}")
    res = client.eql.search(index=index,query=q, size=10000)
    hits = res.raw["hits"]["events"]
    output = {}
    for hit in hits:
        output[hit["_id"]] = hit
    return output

def get_inverse_ids_hacky(client:Elasticsearch, index:str, ids:list):
    q = f"any where true" #todo see #5
    res = client.eql.search(index=index,query=q, size=10000)["hits"]["events"]
    out = {}
    for hit in res:
        if hit["_id"] not in ids:
            out[hit["_id"]] = hit

    return out



def _list_to_string(l):
    out = ""
    for item in l:
        out += f"\"{item}\","
    return out[:-1] if len(out) >1 else ""