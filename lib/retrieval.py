import os

from elasticsearch import Elasticsearch
import toml
import datetime

from lib.esql import res_to_dict


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

def _list_to_string_no_quotes(l):
    """
    convert a list to a comma separated string of list items

    :param l: list to convert to string
    :return: comma separated string of each list item
    """
    out = ""
    for item in l:
        out += f"{item},"
    return out[:-1] if len(out) >1 else ""

class QueryOptions:
    """
    Options for ESQLWrapper Queries
    """
    def __init__(self,
                 date_start:str = "1970-01-01T01:00:00Z",
                 date_end:str = datetime.datetime.now().isoformat(),
                 limit:int=100,
                 blacklist:list=None
                 ):
        """
        :param date_start: start time for the time range
        :param date_end: end time for the time range
        :param limit: limit for events to fetch
        """
        self.date_start = date_start
        self.date_end = date_end
        self.limit = limit
        self.blacklist = blacklist

    def build_args(self):
        out = ""
        if self.blacklist is not None:
            out += f"| DROP {self.blacklist}"
        out += f"| LIMIT {self.limit}"
        return out

    def build_timerange(self):
        return f'| WHERE @timestamp > "{self.date_start}" AND @timestamp < "{self.date_end}"'



class ESQLWrapper:
    def __init__(self, es_url:str, api_key:str):
        self.client = Elasticsearch(
            hosts=[es_url],
            api_key=api_key
        )

    def get_alert_ids(self, index:str, options:QueryOptions):
        """
        get ids of alert sources during a time period

        :param index: index pattern to search
        :param options: options object for the query
        :return: dict of id sets in form {<index>:<set of ids>}
        """
        if options.date_end == "":  # default to ending now
            date_end = datetime.datetime.now(datetime.UTC).isoformat()
        res = self.client.esql.query(query=f"""
        FROM {index} 
        {options.build_timerange()}
        | WHERE event.id != ""
        | KEEP event.id, signal.ancestors.index
        | LIMIT {options.limit}
        """)
        ids = {}
        for event_id, index in res["values"]:
            if index not in ids:
                ids[index] = set()
            ids[index].add(event_id)
        return ids

    def get_inverse_from_ids(self, ids:dict, options:QueryOptions):
        """
        get events not in the ids dict

        :param ids: dict of index:[ids]
        :param options: options object for the query
        :return: list of events
        """
        out = []
        for index, id_list in ids.items():
            res = self.client.esql.query(
                query=f"""
                FROM {index} METADATA _index, _id
                {options.build_timerange()}
                | WHERE event.id not in ({_list_to_string(id_list)})
                {options.build_args()}
                """
            )
            out.extend(res_to_dict(res))
        return out

    def get_from_ids(self, ids:dict, options:QueryOptions):
        """
        get events from their id

        :param ids: dict of index:[ids]
        :param options: options object for the query
        :return: list of events
        """
        out = []
        for index, id_list in ids.items():
            res = self.client.esql.query(
                query=f"""
                FROM {index} METADATA _index, _id
                | WHERE event.id in ({_list_to_string(id_list)})
                {options.build_args()}
                """,
                format="json"
            )
            out.extend(res_to_dict(res))
        return out











