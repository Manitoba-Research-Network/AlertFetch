from elasticsearch import Elasticsearch
import lib.retrieval as retrieval
import os
from dotenv import load_dotenv
import sys
load_dotenv()

RULE_DIR = sys.argv[1]


client = Elasticsearch(
    hosts=[os.getenv("ES_URL")],
    api_key= os.getenv("API_KEY")
)

# Read Rules
rules = retrieval.dir_toml_read(RULE_DIR)
print(rules)

# fetch events for each rule

# fetch non alerted events

# save events


