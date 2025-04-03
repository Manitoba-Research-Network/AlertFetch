from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import sys

from lib.retrieval import get_alert_ids, get_from_ids

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*"
DEFAULT_START_DATE = "NOW() - 5 hour"
DEFAULT_END_DATE = "NOW()"

def main(es_url, api_key, index, start, end):
    client = Elasticsearch(
        hosts=[es_url],
        api_key= api_key
    )


    ids = get_alert_ids(client, index, date_start=start, date_end=end)

    events = get_from_ids(client,ids)

    print(events)


if __name__ == "__main__":
    kwargs = dict(arg.split('=') for arg in sys.argv[1:]) # 0 idx is name of file
    start = kwargs['start'] if "start" in kwargs else DEFAULT_START_DATE
    end = kwargs['end'] if 'end' in kwargs else DEFAULT_END_DATE
    index = kwargs['index'] if 'index' in kwargs else DEFAULT_INDEX_PAT

    load_dotenv()
    main(os.getenv("ES_URL"), os.getenv("API_KEY"), index, start, end)