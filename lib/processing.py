import json

with open("config.json","r") as f:
    exclude = json.load(f)["exclude"]

def clean_entry(entry):
    """
    remove fields from entry that are not wanted for training
    :param entry: entry to clean
    :return: returns the entry without the unwanted fields (note this function operates on the provided entry not a copy)
    """
    for ex in exclude:
        opp = entry
        for field in ex[:-1]:
            if field not in entry:
                entry = None
                break
            opp = entry[field]
        if ex[-1] in opp and opp is not None:
            opp.pop(ex[-1])
    return entry

def clean_entries(entries):
    return [clean_entry(e) for e in entries]
