from elasticsearch import Elasticsearch
import lib.retrieval as retrieval
import os
from dotenv import load_dotenv
import sys

from lib.output import write_json, pretty_print

load_dotenv()

client = Elasticsearch(
    hosts=[os.getenv("ES_URL")],
    api_key= os.getenv("API_KEY")
)


out = client.eql.search(index=".internal.alerts-security.alerts-default-*",query="any where 1==1", size=10000)
pretty_print(out)

for entry in out.raw["hits"]['events']:
    if "event" not in entry["_source"]:
        print("passed")
        continue
    print(entry["_source"]["event"]["id"])
    print(entry["_source"]["@timestamp"])
#print(out)