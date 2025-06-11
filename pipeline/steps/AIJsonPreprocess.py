import json

from pipeline.steps import PipelineStep

PROMPT = "write a 4 sentence summary of this alert data"

class AIJsonPreprocess(PipelineStep):
    def run(self, data):
        json_data = json.dumps(data,sort_keys=True, indent=4)
        return f"{PROMPT}:\n {json_data}"

    def __str__(self):
        return "AI data preprocessor"