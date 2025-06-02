import json

import lib.processing
from ui.app import App
from lib.api import ApiRunner

if __name__ == "__main__":
    with open("apis.json") as f:
        apis = json.load(f)

    api_runner = ApiRunner(apis)

    app = App(api_runner, lib.processing.get_blacklist())



    app.start() # Blocking loop