import os

from elasticsearch import Elasticsearch
import toml
import datetime


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
    for index, id_list in ids.items():
        res = client.eql.search(index=index,query=f"any where event.id not in ({_list_to_string(id_list)}) and @timestamp < \"{date_end}\" and @timestamp > \"{date_start}\"", size=10000)
        out.extend(res.raw["hits"]["events"])
    return out










