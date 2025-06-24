from pipeline.steps import PipelineStep


class PromptAddStep(PipelineStep):
    """adds a prompt to string data"""
    def __init__(self, prompt):
        """
        :param prompt: prompt to add to the data
        """
        self.prompt = prompt

    def run(self, data:str)->str:
        """
        adds a prompt to string data

        :param data: data to add prompt to
        :return: data with prompt added
        """
        return f"{self.prompt}\n{data}"

    def __str__(self):
        return "Add Prompt"