from elastic_transport import ApiResponse
import json


def pretty_print(res: ApiResponse):
    """
    util function for printing a pretty ApiResponse object
    :param res: ApiResponse to print
    """
    print(json.dumps(res.raw,sort_keys=True, indent=4))

def write_json(path, data):
    """
    write dict data to a file

    :param path: path to file
    :param data: data to write to file
    """
    with open(path, "w") as f:
        out = json.dumps(data,sort_keys=True, indent=4)
        f.write(out)

def write_jsonl(path,alert, no_alert):
    """
    write list of alerting and non alerting events to jsonl file with labels for whether they caused alerts

    :param path: filepath to write to
    :param alert: list of events that caused alerts
    :param no_alert: list of events that did not cause alerts
    """
    with open(path, "w") as f:
        for e in alert:
            f.write(json.dumps({"text":json.dumps(e["entry"]), "label":1, **e["meta"]}) + "\n")
        for e in no_alert:
            f.write(json.dumps({"text": json.dumps(e["entry"]), "label": 0, **e["meta"]}) + "\n")

def write_jsonl_no_label(path, events):
    """
    write list of events to a jsonl file

    :param path: filepath to write to
    :param events: list of events
    """
    with open(path, "w") as f:
        for e in events:
            f.write(json.dumps({"text":json.dumps(e["entry"]), **e["meta"]}) + "\n")
