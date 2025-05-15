#!/bin/python
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import sys
import datetime
import argparse

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


    # get alert source ids
    ids = get_alert_ids(client, index, date_start=start, date_end=end)

    # get and clean source events
    events = get_from_ids(client,ids)
    cleaned = clean_entries(events)

    # get and clean non source events
    eventsPass = get_inverse_from_ids(client, ids, date_start=start, date_end=end)
    cleanedPass = clean_entries(eventsPass)

    # output
    write_jsonl(out, cleaned, cleanedPass)
    if no_alert != "": # output separate non-alerting events if path specified
        write_jsonl_no_label(no_alert, cleanedPass)


if __name__ == "__main__":
    #* Load in command line args
    parser = argparse.ArgumentParser(
        prog="AlertFetch CLI",
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

    args = parser.parse_args()
    start = args.start_date
    end = args.end_date
    index = args.index
    out = args.out
    no_alert = args.no_alert

    load_dotenv()
    main(os.getenv("ES_URL"), os.getenv("API_KEY"), index, start, end, out, no_alert)









