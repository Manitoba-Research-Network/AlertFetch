from ai.AiClient import AIClient
from pipeline.steps.PipelineStep import PipelineStep


class AIRunStep(PipelineStep):
    """step for running the ai"""
    def __init__(self, client:AIClient, dev_msg:str):
        """
        :param client: AIClient to use
        :param dev_msg: developer message to use for the query
        """
        self.client = client
        self.dev_msg = dev_msg

    def run(self, data:str)->str:
        """
        run the ai query
        :param data: ai prompt
        :return: ai's response as a string
        """
        return self.client.run_completion(data, self.dev_msg)

    def __str__(self):
        return "AI Runner Step"



