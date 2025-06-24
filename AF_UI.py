import json

from ai.AiClient import AIClient
from lib.api import ApiRunner
from ui.app import App

# Main entry point for the ui
if __name__ == "__main__":
    with open("apis.json") as f:
        apis = json.load(f)

    with open("openai.json") as f:
        ai_conf = json.loads(f.read())

    with open("config.json") as f:
        config = json.load(f)

    api_runner = ApiRunner(apis)
    ai_client = AIClient(**ai_conf, model = "local-model")

    app = App(api_runner, config, ai_client)



    app.start() # Blocking loop