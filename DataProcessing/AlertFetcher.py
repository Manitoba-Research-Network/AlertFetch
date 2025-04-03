from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import sys

from lib.retrieval import get_alert_ids, get_from_ids

load_dotenv()

client = Elasticsearch(
    hosts=[os.getenv("ES_URL")],
    api_key= os.getenv("API_KEY")
)


ids = get_alert_ids(client, ".internal.alerts-security.alerts-default-*")

events = get_from_ids(client,ids)

print(events)