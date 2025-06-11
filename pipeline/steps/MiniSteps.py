from pipeline.steps import PipelineStep


class PrintData(PipelineStep):
    def __init__(self, name):
        self.name = name
    def run(self, data):
        print(data)
        return data
    def __str__(self):
        return self.name