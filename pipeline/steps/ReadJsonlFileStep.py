import json

from pipeline.steps.PipelineStep import PipelineStep


class ReadJsonlFileStep(PipelineStep):
    """step for reading a jsonl file into a list of dicts"""

    def run(self, path:str) -> list[dict]:
        """
        load a jsonl file from a path

        :param path: path to jsonl
        :return: list of dicts from jsonl
        """
        with open(path) as f:
            out = []
            for line in f.readlines():
                out.append(json.loads(line))
            return out

    def __str__(self):
        return "ReadJson"
