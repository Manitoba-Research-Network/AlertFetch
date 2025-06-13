import json

from ai.AiClient import AIClient
from pipeline import *
from pipeline.PipelineRunner import PipelineRunner
from pipeline.PipelineLoopStep import PipelineLoopStep
from pipeline.steps import *

MODEL = "local-model"

with open("openai.json") as f:
    config = json.loads(f.read())


if __name__ == "__main__":
    client = AIClient(**config, model=MODEL)

    multipipe = MultiEventSummary(client)

    print(multipipe.execute("./out/BU_small.jsonl"))

    mega_pipe = MultiEventSingleSummary(
        client,
        "The following are related events, please write a 1 paragraph summary of these events"
    )
    #print(mega_pipe.execute("./out/BU_small.jsonl"))


