from elasticsearch import Elasticsearch
import lib.retrieval as retrieval
import os
from dotenv import load_dotenv
import sys

from lib.output import write_json, pretty_print
from lib.retrieval import get_alert_ids

load_dotenv()

client = Elasticsearch(
    hosts=[os.getenv("ES_URL")],
    api_key= os.getenv("API_KEY")
)


ids = get_alert_ids(client, ".internal.alerts-security.alerts-default-*")

print(ids)