#!/bin/python
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import sys
import datetime

from lib.output import write_jsonl, write_jsonl_no_label
from lib.processing import clean_entry, clean_entries
from lib.retrieval import get_alert_ids, get_from_ids, get_inverse_from_ids

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*"
DEFAULT_START_DATE = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=5)).isoformat()
DEFAULT_END_DATE = datetime.datetime.now(datetime.UTC).isoformat()

def main(es_url, api_key, index, start, end, out, no_alert = ""):
    client = Elasticsearch(
        hosts=[es_url],
        api_key= api_key
    )


    ids = get_alert_ids(client, index, date_start=start, date_end=end)

    events = get_from_ids(client,ids)
    cleaned = clean_entries(events)

    eventsPass = get_inverse_from_ids(client, ids, date_start=start, date_end=end)
    cleanedPass = clean_entries(eventsPass)

    write_jsonl(out, cleaned, cleanedPass)
    if no_alert != "":
        write_jsonl_no_label(no_alert, cleanedPass)


if __name__ == "__main__":
    #* Load in command line args
    kwargs = dict(arg.split('=') for arg in sys.argv[1:]) # 0 idx is name of file
    start = kwargs['start'] if "start" in kwargs else DEFAULT_START_DATE
    end = kwargs['end'] if 'end' in kwargs else DEFAULT_END_DATE
    index = kwargs['index'] if 'index' in kwargs else DEFAULT_INDEX_PAT
    if "out" not in kwargs:
        print("'out' is a required keyword parameter")
        exit(1)
    out = kwargs['out']
    no_alert = kwargs['no_alert'] if 'no_alert' in kwargs else ""

    load_dotenv()
    main(os.getenv("ES_URL"), os.getenv("API_KEY"), index, start, end, out, no_alert)