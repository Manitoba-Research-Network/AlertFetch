#!/bin/python
import json

import datetime
import argparse

import lib.output
from lib.output import write_jsonl, write_jsonl_no_label
from lib.processing import extract_metadata
from lib.retrieval import ESQLWrapper, QueryOptions

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*"
DEFAULT_START_DATE = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=5)).isoformat()
DEFAULT_END_DATE = datetime.datetime.now(datetime.UTC).isoformat()

with open("config.json", "r") as f:
    config = json.load(f)

def main(client:ESQLWrapper, q_options:QueryOptions,index, out, api, no_alert = ""):


    # get alert source ids
    ids = client.get_alert_ids(index, q_options)

    # get and clean source events
    events = client.get_from_ids(ids, q_options)
    cleaned = extract_metadata(events, api)

    # get and clean non source events
    eventsPass = client.get_inverse_from_ids(ids, q_options)
    cleanedPass = extract_metadata(eventsPass, api)

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
    q_options = QueryOptions(
        date_start=args.start_date,
        date_end=args.end_date,
        limit=args.limit,
        blacklist=config["exclude"]
    )
    if args.api == "ALL": # run for all
        for key, val in apis.items():
            client = ESQLWrapper(val["uri"], val["key"])
            main(client, q_options, index, out, key, no_alert)
        if args.combine:
            lib.output.combine_jsonl(out)
    else: # run for single
        try:
            api = apis[args.api]
        except KeyError:
            print(f"API '{args.api}' was not found in the apis.json file.")
            exit(1)
        client = ESQLWrapper(api["uri"], api["key"])
        main(client, q_options, index, out, args.api, no_alert)










