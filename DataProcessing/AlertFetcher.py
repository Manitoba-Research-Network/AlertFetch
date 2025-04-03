from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import sys

from lib.retrieval import get_alert_ids, get_from_ids


def main(es_url, api_key, **kwargs):
    client = Elasticsearch(
        hosts=[es_url],
        api_key= api_key
    )


    ids = get_alert_ids(client, ".internal.alerts-security.alerts-default-*")

    events = get_from_ids(client,ids)

    print(events)


if __name__ == "__main__":
    load_dotenv()
    main(os.getenv("ES_URL"), os.getenv("API_KEY"))