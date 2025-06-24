from typing import Iterable

from pipeline import PipelineRunner
from pipeline.steps import PipelineStep


class PipelineLoopStep(PipelineStep):
    """step for executing a sub pipeline for each entry in an iterable"""
    def __init__(self, pipeline: PipelineRunner, name: str):
        """
        :param pipeline: pipeline to execute
        :param name: name of the step
        """
        self.pipeline = pipeline
        self.name = name

    def run(self, data:Iterable):
        """
        execute pipeline for each entry in an iterable

        :param data: iterable data to run with
        :return: list of outputs from each run
        """
        out = []
        for item in data:
            print(f"<{self}> Running {self.pipeline}")
            out.append(self.pipeline.execute(item))
            print(f"</{self}> Done")
        return out



    def __str__(self):
        return self.name