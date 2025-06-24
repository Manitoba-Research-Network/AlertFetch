# This file contains various prefab pipelines, mostly for ai execution
from pipeline.PipelineRunner import PipelineRunner
from pipeline.PipelineLoopStep import PipelineLoopStep
from pipeline.steps import *


def MultiEventSummary(client:AIClient,
                      prompt="The following are summaries from alerts that are all related to each other, write a brief summary of these summaries",
                      mode: str = AIJsonPreprocess.MODE_JSON,
                      **kwargs
                      ) -> PipelineRunner:
    """
    summarize multiple events using intermediate summaries for each event
    """

    pipeline = _standard_preprocess(mode)

    pipeline.add_step(PromptAddStep("write a 4 sentence summary of this alert data"))  # add prompt to data
    pipeline.add_step(PrintData("Print Prompt"))
    pipeline.add_step(AIRunStep(client, "you are a security expert"))  # summarize the event

    multipipe = PipelineRunner("MultiEventRunner")
    multipipe.add_step(ReadJsonlFileStep())
    multipipe.add_step(PipelineLoopStep(pipeline, "SingleSummary"))
    multipipe.add_step(AggregateResponsesStep("Summary #"))
    multipipe.add_step(PromptAddStep(prompt))
    multipipe.add_step(PrintData("Aggregate Summary Prompt"))
    multipipe.add_step(AIRunStep(client, "you are a security expert"))

    return multipipe

def MultiEventSingleSummary(
        client:AIClient,
        prompt: str = "The following are related events, please write a brief summary of these events",
        mode:str = AIJsonPreprocess.MODE_JSON,
        **kwargs
) -> PipelineRunner:
    """
    summarize all events in single ai prompt
    """
    json_format_pipe = _standard_preprocess(mode)

    mega_pipe = PipelineRunner("MultiEvent1Summary")
    mega_pipe.add_step(ReadJsonlFileStep())
    mega_pipe.add_step(PipelineLoopStep(json_format_pipe, "format json"))
    mega_pipe.add_step(AggregateResponsesStep("Event #"))
    mega_pipe.add_step(PromptAddStep(prompt))
    mega_pipe.add_step(PrintData("Event Summary Prompt"))
    mega_pipe.add_step(AIRunStep(client, "you are a security expert"))

    return mega_pipe

def intermediate_summary(
        client:AIClient,
        prompt: str = "The following are summaries from alerts that are all related to each other, write a brief summary of these summaries",
        compression: list[int] = 1,
        depth: int = 0,
        prompt_intermediate: str = "The following are related events, please write a brief summary of these events",
        mode:str = AIJsonPreprocess.MODE_JSON,
        **kwargs
) -> PipelineRunner:
    """
    run a summary using 1 or more intermediate summary layers
    :param client: ai client to use
    :param prompt: prompt for final summary
    :param compression: number of summaries/events to combine in each intermediate summary layer
    :param depth: number of intermediate summary layers
    :param prompt_intermediate: prompt to use in intermediate summaries
    :param mode: mode to use for json processing
    :param kwargs: additional args
    :return: PipelineRunner with given configuration
    """
    pipeline = _standard_preprocess(mode)

    multipipe = PipelineRunner("MultiEventRunner")
    multipipe.add_step(ReadJsonlFileStep())
    multipipe.add_step(PipelineLoopStep(pipeline, "ReadJsons"))  # finish parsing
    for level in range(depth):
        multipipe.add_step(ListSplitStep(compression[level]))
        multipipe.add_step(PipelineLoopStep(
            _intermediate_pipe(client, prompt_intermediate),
            f"Intermediate Summary, Level {level}")
        )

    multipipe.add_step(AggregateResponsesStep("Summary #"))
    multipipe.add_step(PromptAddStep(prompt))
    multipipe.add_step(PrintData("Aggregate Summary Prompt"))
    multipipe.add_step(AIRunStep(client, "you are a security expert"))

    return multipipe


def _standard_preprocess(mode):
    pipeline = PipelineRunner("Parse inner json")
    pipeline.add_step(
        LambdaPipelineStep("Get First List Value & Parse to json", lambda x: json.loads(x["text"])))  # get first event
    pipeline.add_step(AIJsonPreprocess(mode))  # get the AI input ready
    return pipeline


def _intermediate_pipe(client:AIClient, prompt:str = "write a 4 sentence summary of this alert data") -> PipelineRunner:
    pipeline = PipelineRunner("SummarizeEvent")
    pipeline.add_step(AggregateResponsesStep("Summary #"))
    pipeline.add_step(PromptAddStep(prompt))  # add prompt to data
    pipeline.add_step(PrintData("Print Prompt"))
    pipeline.add_step(AIRunStep(client, "you are a security expert"))  # summarize the event
    return pipeline
