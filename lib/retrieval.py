import os

from elasticsearch import Elasticsearch
import toml
import datetime


def _list_to_string(l):
    """
    convert a list to a comma separated string of list items

    :param l: list to convert to string
    :return: comma separated string of each list item
    """
    out = ""
    for item in l:
        out += f"\"{item}\","
    return out[:-1] if len(out) >1 else ""

def get_alert_ids(client:Elasticsearch, index:str, date_start:str = "1970-01-01T01:00:00Z", date_end:str = ""):
    """
    get ids of alert sources during a time period

    :param client: client to use for the search
    :param index: index pattern to search
    :param date_start: start time for the time range
    :param date_end:  end time for the time range
    :return: dict of id sets in form {<index>:<set of ids>}
    """
    if date_end == "": # default to ending now
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

def get_from_ids(client:Elasticsearch, ids:dict, limit:int=100):
    """
    get source events from alerts

    :param client: client to use for the request
    :param ids: dict of id sets
    :param limit: limit on number of events to fetch
    :return: list of source events
    """
    out = []
    for index, id_list in ids.items():
        res = client.eql.search(index=index,query=f"any where event.id in ({_list_to_string(id_list)})", size=limit)
        out.extend(res.raw["hits"]["events"])
    return out


def get_inverse_from_ids(client:Elasticsearch, ids:dict, date_start:str = "1970-01-01T01:00:00Z", date_end:str = datetime.datetime.now().isoformat(), limit:int = 100):
    """
    get events that did not trigger alerts within a time range

    :param limit: limit on number of events to fetch
    :param client: client to use for the request
    :param ids: dict of id sets
    :param date_start: start time for the time range
    :param date_end:  end time for the time range
    :return: list of events
    """
    out = []
    for index, id_list in ids.items():
        res = client.eql.search(index=index,query=f"any where event.id not in ({_list_to_string(id_list)}) and @timestamp < \"{date_end}\" and @timestamp > \"{date_start}\"", size=limit)
        out.extend(res.raw["hits"]["events"])
    return out










