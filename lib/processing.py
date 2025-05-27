def extract_metadata(entries, api = None):
    out = []
    for e in entries:
        clean = {"meta":{"id": e["_id"], "idx": e["_index"]}, "entry":{**e}}
        clean["entry"].pop("_id")
        clean["entry"].pop("_index")
        if api is not None:
            clean["meta"]["api"] = api
        out.append(clean)
    return out