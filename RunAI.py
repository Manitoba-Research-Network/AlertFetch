import json

from ai.AiClient import AIClient
from pipeline.PipelineRunner import PipelineRunner
from pipeline.steps import *

MODEL = "local-model"

with open("openai.json") as f:
    config = json.loads(f.read())


if __name__ == "__main__":
    client = AIClient(**config, model=MODEL)
    pipeline = PipelineRunner("AIRun")
    pipeline.add_step(ReadJsonlFileStep()) # read input file
    pipeline.add_step(LambdaPipelineStep("Get First List Value",lambda x: x[0])) # get first event
    pipeline.add_step(AIJsonPreprocess()) # get the AI input ready
    pipeline.add_step(AIRunStep(client, "you are a security expert")) # summarize the event


    print(pipeline.execute("./out/MRNet.jsonl"))
