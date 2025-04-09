from elastic_transport import ApiResponse
import json


def pretty_print(res: ApiResponse):
    print(json.dumps(res.raw,sort_keys=True, indent=4))

def write_json(path, data):
    with open(path, "w") as f:
        out = json.dumps(data,sort_keys=True, indent=4)
        f.write(out)

def write_jsonl(path,alert, no_alert):
    with open(path, "w") as f:
        for e in alert:
            f.write(json.dumps({"text":json.dumps(e), "label":1}) + "\n")
        for e in no_alert:
            f.write(json.dumps({"text": json.dumps(e), "label": 0}) + "\n")
