def res_to_dict(res) -> list:
    """
    convert the response from an esql query to a dict
    :param res:
    :return:
    """
    cols = res['columns']
    keys = [key["name"] for key in cols]
    vals = res['values']

    return [{k:v for (k,v) in zip(keys, entry)} for entry in vals] # "Idiomatic Python"
    # The above takes each entry in values and zips its values into a list of tuples, the for loop converts each tuple
    # to a key value pair (which is output to a dict)