import os

from elasticsearch import Elasticsearch
import toml
import datetime

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

def get_alert_ids(client:Elasticsearch, index:str, date_start:str = "1970-01-01T01:00:00Z", date_end:str = ""):
    if date_end == "":
        date_end = datetime.datetime.now(datetime.UTC).isoformat()
    res = client.esql.query(query=f"""
    FROM {index} 
    | WHERE @timestamp > "{date_start}" AND @timestamp < "{date_end}"
    | WHERE event.id != ""
    | KEEP event.id, signal.ancestors.index
    | LIMIT 10000
    """)
    ids = {}
    for event_id, index in res["values"]:
        if index not in ids:
            ids[index] = set()
        ids[index].add(event_id)
    return ids

def get_from_ids(client:Elasticsearch, ids:dict):
    out = []
    for index, id_list in ids.items():
        res = client.eql.search(index=index,query=f"any where event.id in ({_list_to_string(id_list)})", size=10000)
        out.extend(res.raw["hits"]["events"])
    return out


def get_inverse_from_ids(client:Elasticsearch, ids:dict, date_start:str = "1970-01-01T01:00:00Z", date_end:str = datetime.datetime.now().isoformat()):
    out = []
    for index, id_list in ids.items(): # todo add datetime to this
        res = client.eql.search(index=index,query=f"any where event.id not in ({_list_to_string(id_list)}) and @timestamp < \"{date_end}\" and @timestamp > \"{date_start}\"", size=10000)
        out.extend(res.raw["hits"]["events"])
    return out










