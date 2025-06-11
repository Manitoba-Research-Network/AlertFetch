from typing import Iterable

from pipeline import PipelineRunner
from pipeline.steps import PipelineStep


class PipelineLoopStep(PipelineStep):
    def __init__(self, pipeline: PipelineRunner, name: str):
        self.pipeline = pipeline
        self.name = name

    def run(self, data:Iterable):
        out = []
        for item in data:
            print(f"<{self}> Running {self.pipeline}")
            out.append(self.pipeline.execute(item))
            print(f"</{self}> Done")
        return out



    def __str__(self):
        return self.name