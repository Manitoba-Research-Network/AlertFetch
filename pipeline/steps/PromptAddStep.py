from pipeline.steps import PipelineStep


class PromptAddStep(PipelineStep):
    def __init__(self, prompt):
        self.prompt = prompt

    def run(self, data):
        return f"{self.prompt}\n{data}"

    def __str__(self):
        return "Add Prompt"