import json

import lib.processing
from ai.AiClient import AIClient
from ui.app import App
from lib.api import ApiRunner

if __name__ == "__main__":
    with open("apis.json") as f:
        apis = json.load(f)

    with open("openai.json") as f:
        config = json.loads(f.read())

    api_runner = ApiRunner(apis)
    ai_client = AIClient(**config, model = "local-model")

    app = App(api_runner, lib.processing.get_blacklist(), ai_client)



    app.start() # Blocking loop