import json

def clean_entries(entries, api = None):
    """
    removes null fields and extracts metadata from each entry
    :param entries:  list of entries
    :param api: api to put in metadata
    :return: cleaned entries
    """
    out = remove_null_fields(entries)
    return extract_metadata(out, api)

def extract_metadata(entries, api = None):
    """
    extracts metadata from each entry
    :param entries: entries to extract metadata from
    :param api: api for the metadata
    :return: dict of form {meta:[METADATA], entry:[ENTRY]}
    """
    out = []
    for e in entries:
        clean = {"meta": {"id": e["_id"], "idx": e["_index"]}, "entry": {**e}} # initial format
        #remove metadata from entry
        clean["entry"].pop("_id")
        clean["entry"].pop("_index")
        #add api if present
        if api is not None:
            clean["meta"]["api"] = api
        out.append(clean)
    return out

def remove_null_fields(entries:list):
    """
    removes null fields from each entry
    :param entries: entries to remove null fields from
    :return: list of entries with null fields removed
    """
    out = []
    for e in entries: # this is O(k*n) but k << n so should generally still be fine
        out.append({k:v for (k,v) in e.items() if v is not None})
    return out