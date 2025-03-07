from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
from lib.output import pretty_print
load_dotenv()


client = Elasticsearch(
    hosts=[os.getenv("ES_URL")],
    api_key= os.getenv("API_KEY")
)

res= client.search(index="logs-omm_one", q='process where host.os.type == "windows" and event.type == "start" and process.parent.name : "Zoom.exe" and process.name : ("cmd.exe", "powershell.exe", "pwsh.exe", "powershell_ise.exe")')

print(len(res.raw["hits"]["hits"]))



pretty_print(res)