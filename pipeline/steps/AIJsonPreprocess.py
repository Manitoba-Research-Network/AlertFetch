import json

from pipeline.steps import PipelineStep

class AIJsonPreprocess(PipelineStep):
    """
    class for providing various json processing methods such as json pretty printing or converting to newline yaml ish
    """
    MODE_JSON = "json"
    MODE_NEWLINE = "newline"

    def __init__(self, mode:str = MODE_JSON):
        """
        :param mode: preprocessing mode to use, json (just output the prettified json) or newline
                     (output the fields as a newline seperated string)
        """
        self.mode = mode
        match mode:
            case "json":
                runner = self._for_json
            case "newline":
                runner = self._for_newline
                pass
            case _:
                raise ValueError(f"Invalid mode: {mode}")

        self.runner = runner


    def run(self, data:list[str])->str:
        """
        aggregates the string in data into a single string
        :param data: list of strings to aggregate
        :return: single string
        """
        return self.runner(data)

    def _for_json(self,data):
        return json.dumps(data,sort_keys=True, indent=4)

    def _for_newline(self,data):
        out = ""
        for k,v in data.items():
            out += f"{k}: {v}\n"
        return out

    def __str__(self):
        return f"AI data preprocessor (mode: {self.mode})"