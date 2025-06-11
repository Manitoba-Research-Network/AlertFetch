import json

from pipeline.steps import PipelineStep

class AIJsonPreprocess(PipelineStep):
    def run(self, data):
        return json.dumps(data,sort_keys=True, indent=4)# todo this likely should do more

    def __str__(self):
        return "AI data preprocessor"