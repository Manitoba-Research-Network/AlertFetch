import json

from ai.AiClient import AIClient
from pipeline.PipelineRunner import PipelineRunner
from pipeline.PipelineLoopStep import PipelineLoopStep
from pipeline.steps import *

MODEL = "local-model"

with open("openai.json") as f:
    config = json.loads(f.read())


if __name__ == "__main__":
    client = AIClient(**config, model=MODEL)

    pipeline = PipelineRunner("SummarizeEvent")
    pipeline.add_step(LambdaPipelineStep("Get First List Value & Parse to json",lambda x: json.loads(x["text"]))) # get first event
    pipeline.add_step(AIJsonPreprocess()) # get the AI input ready
    pipeline.add_step(PromptAddStep("write a 4 sentence summary of this alert data")) # add prompt to data
    pipeline.add_step(PrintData("Print Prompt"))
    pipeline.add_step(AIRunStep(client, "you are a security expert")) # summarize the event

    multipipe = PipelineRunner("MultiEventRunner")
    multipipe.add_step(ReadJsonlFileStep())
    multipipe.add_step(PipelineLoopStep(pipeline, "SingleSummary"))
    multipipe.add_step(AggregateResponsesStep("Summary #"))
    multipipe.add_step(PromptAddStep("The following are summaries from alerts that are all related to each other, write a brief summary of these summaries"))
    multipipe.add_step(PrintData("Aggregate Summary Prompt"))
    multipipe.add_step(AIRunStep(client, "you are a security expert"))

    print(multipipe.execute("./out/BU_small.jsonl"))
