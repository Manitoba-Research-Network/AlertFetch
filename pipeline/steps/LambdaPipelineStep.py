from typing import Callable

from pipeline.steps.PipelineStep import PipelineStep


class LambdaPipelineStep(PipelineStep):
    """step for arbitrary function execution, should be used for simple lambdas"""
    def __init__(self, name:str, cb:Callable[[any],any]):
        """
        :param name: name of the step
        :param cb: callback function to use during run
        """
        self.name = name
        self.cb = cb

    def __str__(self):
        return self.name

    def run(self, data:any)->any:
        """
        run the data through the callback
        :param data: data to use
        :return: result from callback
        """
        return self.cb(data)