import json
import os


def pretty_print(json_data):
    """
    pretty print dict
    :param json_data: dict to print
    """
    print(json.dumps(json_data,sort_keys=True, indent=4))

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

def combine_jsonl(path):
    """
    combine jsonl files in a directory into a single jsonl file (`combined.jsonl`)
    :param path: path to directory to operate on
    """
    with open(path + "combined.jsonl", "w") as out_f:
        for file in os.listdir(path):
            if file == "combined.jsonl":
                continue # ignore the output file
            with open(path + "/" + file, "r") as in_f:
                out_f.write(in_f.read())













