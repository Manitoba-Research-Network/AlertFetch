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


# todo move to library
# todo time filtering
res = client.esql.query(query="""FROM .internal.alerts-security.alerts-default-* 
| WHERE @timestamp < "2025-04-01T16:47:44Z" 
| WHERE event.id != ""
| KEEP event.id
| LIMIT 10000
""")
print(res)

ids = set(i[0] for i in res["values"]) # ESQL returns a list of lists this decomposes the inner lists to a list

print(ids)