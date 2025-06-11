from typing import Callable

from pipeline.steps.PipelineStep import PipelineStep


class LambdaPipelineStep(PipelineStep):
    def __init__(self, name:str, cb:Callable[[any],any]):
        self.name = name
        self.cb = cb

    def __str__(self):
        return self.name

    def run(self, data):
        return self.cb(data)