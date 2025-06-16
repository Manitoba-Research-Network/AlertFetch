
from elasticsearch import Elasticsearch
import datetime

from lib.esql import res_to_dict

def _flatten_get_response(res):
    """
    flattens a dict so it is only 1 layer deep, by making field '.' seperated

    :param res: dict to flatten
    :return: flattened dict
    """
    inner = res["_source"] # we only care about the
    inner["_id"] = res["_id"]
    inner["_index"] = res["_index"]
    return _flatten_recurse_helper(inner)

def _flatten_recurse_helper(inner, prefix=""):
    """
    helper function to flatten a dict recursively

    :param inner: inner dict
    :param prefix: prefix string
    :return: flattened dict
    """
    out = {}
    for k, v in inner.items():
        if isinstance(v, dict):
            out.update(_flatten_recurse_helper(v, prefix=f"{prefix}{k}."))
        else:
            out[f"{prefix}{k}"] = v
    return out

def _get_time_around(time:str, delta:int)-> (str,str):
    """
    get a time range around a specified time

    :param time: time to get around
    :param delta: difference around the given time
    :return: tuple of (start, end)
    """
    date = datetime.datetime.fromisoformat(time)
    timedelta = datetime.timedelta(seconds=delta)

    return (date - timedelta).isoformat(), (date + timedelta).isoformat()

def _fields_to_equality(fields:dict):
    """
    convert fields to equality strings
    :param fields: dict of key values to equal
    :return: list of equality strings
    """
    return [f'{k}=="{v}"' for k,v in fields.items()]



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
                 blacklist:list=None,
                 include:bool=False
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
        self.include = include

    def build_args(self):
        out = ""
        if self.blacklist is not None:
            out += f"| {'KEEP' if self.include else 'DROP'} {_list_to_string_no_quotes(self.blacklist)}"
            if self.include:
                out += ",_id,_index" # these always need to be kept, this might be slightly less efficient since it's on a separate line though

        out += f"| LIMIT {self.limit}"
        return out

    def build_timerange(self):
        return f'| WHERE @timestamp > "{self.date_start}" AND @timestamp < "{self.date_end}"'


def _ctx_query(fields:dict, ctx_window:int, timestamp:str, index:str)->str:
    """
    get the query for a event group context
    :param fields: fields to match
    :param ctx_window: context time delta
    :param timestamp: time to get around
    :param index: index to pull from
    :return: string query
    """
    start, end = _get_time_around(timestamp, ctx_window)

    field_cond = ""
    for e in _fields_to_equality(fields):
        field_cond += f"| WHERE {e}\n"

    return f"""
    FROM {index} METADATA _id, _index
    | WHERE @timestamp > "{start}" AND @timestamp < "{end}"
    {field_cond}
    """


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

    def count_from_ids(self, ids:dict, options:QueryOptions)->int:
        out = 0
        for index, id_list in ids.items():
            res = self.client.esql.query(
                query=f"""
                FROM {index} METADATA _index, _id
                | WHERE event.id in ({_list_to_string(id_list)})
                {options.build_args()}
                | STATS COUNT(*)
                """
            )
            out += res['values'][0][0]
        return out

    def count_inverse_from_ids(self, ids:dict, options:QueryOptions)->int:
        out = 0
        for index, id_list in ids.items():
            res = self.client.esql.query(
                query=f"""
                FROM {index} METADATA _index, _id
                {options.build_timerange()}
                | WHERE event.id not in ({_list_to_string(id_list)})
                {options.build_args()}
                | STATS COUNT(*)
                """
            )
            out += res['values'][0][0]
        return out

    def get_event_by_id(self, idd, index:str):
        """
        get a single event by _id

        :param index: index to query
        :param idd: id of the event to get
        :return: the event object
        """
        event = self.client.get(
            index=index,
            id=idd
        )

        return _flatten_get_response(event)

    def count_ctx(self, fields:dict, ctx_window:int, timestamp:str, index:str)->int:
        """
        count the number of events with a certain context
        :param fields: fields and values to match
        :param ctx_window: time around timestamp to search
        :param timestamp: timestamp to search around
        :param index: index to query
        :return: number of events in context
        """
        res = self.client.esql.query(
            query=_ctx_query(fields, ctx_window, timestamp, index) + "|STATS COUNT(*)"
        )
        return res['values'][0][0]

    def get_ctx(self, fields:dict, ctx_window:int, timestamp:str, index:str, options:QueryOptions):
        """
        get events in a context window
        :param fields: fields and values to match
        :param ctx_window: time around timestamp to search
        :param timestamp: timestamp to search around
        :param index: index to query
        :param options: options object for the query
        :return: list of events in context
        """
        res = self.client.esql.query(
            query=_ctx_query(fields, ctx_window, timestamp, index) + options.build_args()
        )
        return res_to_dict(res)












