def res_to_dict(res) -> list:
    cols = res['columns']
    keys = [key["name"] for key in cols]
    vals = res['values']

    return [{k:v for (k,v) in zip(keys, entry)} for entry in vals] # this is slightly cursed, it converts what is essentially a csv into a dict with the headers for keys
