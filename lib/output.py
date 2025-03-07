from elastic_transport import ApiResponse
import json


def pretty_print(res: ApiResponse):
    print(json.dumps(res.raw,sort_keys=True, indent=4))
