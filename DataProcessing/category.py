import json

from elasticsearch import Elasticsearch
import lib.retrieval as retrieval
import os
from dotenv import load_dotenv
import sys

from lib.output import write_json

load_dotenv()

RULE_DIR = sys.argv[1]
OUT_FILE = "output.json"
OUT_PASS_FILE = "pass.json"
ERROR_FILE = "error.json"
INDICES = ["logs-omm_one","logs-omm_two","logs-omm_three","logs-omm_four","logs-omm_five","logs-omm_six","logs-omm_seven","logs-omm_eight"]
#INDICES = ["logs-omm_one"]


client = Elasticsearch(
    hosts=[os.getenv("ES_URL")],
    api_key= os.getenv("API_KEY")
)

# Read Rules
rules = retrieval.dir_toml_read(RULE_DIR)


def get_data(index):
    # fetch events for each rule
    failures = []
    events_alert = {}
    print(rules)
    for rule in rules:
        try:
            # todo at some point this should actually handle other query types see: IPG5/scripts #4
            if rule["rule"]["lang"] != "eql":
                continue  # skip any non eql queries

            events_alert = dict(events_alert, **retrieval.get_events(client, index, rule["rule"]["query"]))

        except Exception as e:
            print(f"failed: {rule}")
            print(f"error: {e}")
            failures.append({"rule": rule, "error": str(e)})
    print(events_alert)
    # fetch non alerted events
    events_non_alert = retrieval.get_inverse_ids_hacky(client, index, list(events_alert.keys()))
    print(events_non_alert)
    # save events
    return events_alert, events_non_alert, failures


i = 1
for idx in INDICES:

    events_alert, events_non_alert, failures = get_data(idx)
    write_json(str(i) + OUT_FILE, events_alert)
    write_json(str(i) + ERROR_FILE, {"fails": failures})
    write_json(str(i) + OUT_PASS_FILE, events_non_alert)
    i+=1

