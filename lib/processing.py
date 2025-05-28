def clean_entries(entries, api = None):
    out = remove_null_fields(entries)
    return extract_metadata(out, api)

def extract_metadata(entries, api = None):
    out = []
    for e in entries:
        clean = {"meta": {"id": e["_id"], "idx": e["_index"]}, "entry": {**e}}
        clean["entry"].pop("_id")
        clean["entry"].pop("_index")
        if api is not None:
            clean["meta"]["api"] = api
        out.append(clean)
    return out

def remove_null_fields(entries:list):
    out = []
    for e in entries: # this is O(k*n) but k << n so should generally still be fine
        out.append({k:v for (k,v) in e.items() if v is not None})
    return out