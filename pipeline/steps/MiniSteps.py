from pipeline.steps import PipelineStep


class PrintData(PipelineStep):
    def __init__(self, name):
        self.name = name
    def run(self, data):
        print(data)
        return data
    def __str__(self):
        return self.name

class WriteData(PipelineStep):
    def __init__(self, path):
        self.path = path
    def run(self, data):
        with open(self.path, 'w') as f:
            f.write(data)
        return data

    def __str__(self):
        return "Write Data"