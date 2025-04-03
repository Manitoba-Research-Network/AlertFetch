exclude = [
    ["_source", "ecs"],
    ["_index"]
]

#todo this may need to be moved to a class so the field list can be defined by a config file (if we want that)
def clean_entry(entry):
    """
    remove fields from entry that are not wanted for training
    :param entry: entry to clean
    :return: returns the entry without the unwanted fields (note this function operates on the provided entry not a copy)
    """
    for ex in exclude:
        opp = entry
        for field in ex[:-1]:
            opp = entry[field]
        opp.pop(ex[-1])
    return entry

def zip_alerted(alert, no_alert):
    """
    create training ready dataset from 2 lists of events
    :param alert: list of events that created an alert
    :param no_alert: list of events that didn't create an alert
    :return: todo
    """
    pass
