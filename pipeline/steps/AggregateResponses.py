from pipeline.steps import PipelineStep


class AggregateResponsesStep(PipelineStep):
    def __init__(self, prefix:str):
        self.prefix = prefix

    def run(self, data:list[str])->str:
        """
        takes in a list of strings and makes them into one string with numbered headers
        :param data: list of strings
        :return: single string
        """
        out = ""
        for n,entry in enumerate(data):
            tabbed = '\t'.join(entry.splitlines(True))
            out += f"{self.prefix}{n}\n{tabbed}\n"
        return out

    def __str__(self):
        return "Aggregate Responses"