#!/bin/python
import json

from elasticsearch import Elasticsearch
import datetime
import argparse

import lib.output
from lib.output import write_jsonl, write_jsonl_no_label
from lib.processing import clean_entry, clean_entries
from lib.retrieval import get_alert_ids, get_from_ids, get_inverse_from_ids

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*"
DEFAULT_START_DATE = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=5)).isoformat()
DEFAULT_END_DATE = datetime.datetime.now(datetime.UTC).isoformat()

with open("config.json", "r") as f:
    config = json.load(f)

def main(es_url, api_key, index, start, end, out, api, no_alert = "", limit = 100):
    client = Elasticsearch(
        hosts=[es_url],
        api_key= api_key
    )


    # get alert source ids
    ids = get_alert_ids(client, index, date_start=start, date_end=end)

    # get and clean source events
    events = get_from_ids(client,ids, limit=limit)
    cleaned = clean_entries(events, api)

    # get and clean non source events
    eventsPass = get_inverse_from_ids(client, ids, date_start=start, date_end=end, limit=limit)
    cleanedPass = clean_entries(eventsPass, api)

    # output
    write_jsonl(out + f"{api}.jsonl", cleaned, cleanedPass)
    if no_alert != "": # output separate non-alerting events if path specified
        write_jsonl_no_label(no_alert+ f"no-alert_{api}.jsonl", cleanedPass)

def get_apis() -> dict:
    with open("apis.json") as f:
        return json.loads(f.read())


if __name__ == "__main__":
    #* Load in command line args
    parser = argparse.ArgumentParser(
        prog="./AlertFetcher.py",
        description='Script for fetching alerts from Elasticsearch'
    )

    parser.add_argument('-s', '--start-date',
                        default=DEFAULT_START_DATE,
                        help='Start date for alerts',
                        type=str)
    parser.add_argument('-e', '--end-date',
                        default=DEFAULT_END_DATE,
                        help='End date for alerts',
                        type=str)
    parser.add_argument('-o', '--out',
                        required=True,
                        help='Output file path',
                        type=str)
    parser.add_argument('-i', '--index',
                        default=DEFAULT_INDEX_PAT,
                        help='Elasticsearch index pattern',
                        type=str)
    parser.add_argument('--no-alert',
                        default="",
                        help='path to output non alerting events',
                        type=str)
    parser.add_argument('api',
                        type=str,
                        help='API to use from apis.json. use `ALL` to run on all APIs')
    parser.add_argument('-l','--limit',
                         type=int,
                         default=10000,
                         help='Limit on event queries')
    parser.add_argument('--combine',
                        default=False,
                        type=bool,
                        help='Combine all apis into single file `combined.jsonl`',
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    start = args.start_date
    end = args.end_date
    index = args.index
    out = args.out
    no_alert = args.no_alert

    apis = get_apis()
    if args.api == "ALL": # run for all
        for key, val in apis.items():
            main(val["uri"], val["key"], index, start, end, out, key, no_alert, args.limit)
        if args.combine:
            lib.output.combine_jsonl(out)
    else: # run for single
        try:
            api = apis[args.api]
        except KeyError:
            print(f"API '{args.api}' was not found in the apis.json file.")
            exit(1)
        main(api["uri"], api["key"], index, start, end, out, args.api, no_alert, limit = args.limit)










