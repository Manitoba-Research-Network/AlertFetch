from ai.AiClient import AIClient
from pipeline.steps.PipelineStep import PipelineStep


class AIRunStep(PipelineStep):
    def __init__(self, client:AIClient, dev_msg:str):
        self.client = client
        self.dev_msg = dev_msg

    def run(self, data):
        return self.client.run_completion(data, self.dev_msg)

    def __str__(self):
        return "AI Runner Step"



