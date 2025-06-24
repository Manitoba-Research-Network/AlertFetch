"""
Small step classes that dont need a dedicated file
"""
from pipeline.steps import PipelineStep


class PrintData(PipelineStep):
    """step for printing the data with pass through"""
    def __init__(self, name):
        """
        :param name: name of the step
        """
        self.name = name

    def run(self, data):
        """print the data then return it (no processing)"""
        print(data)
        return data
    def __str__(self):
        return self.name

class WriteData(PipelineStep):
    """step for writing the data with pass through"""
    def __init__(self, path):
        """
        :param path: path to write to
        """
        self.path = path
    def run(self, data):
        """
        writes the data then return it (no processing)
        :param data: data to write
        :return: data (unchanged)
        """
        with open(self.path, 'w') as f:
            f.write(data)
        return data

    def __str__(self):
        return "Write Data"

class ListSplitStep(PipelineStep):
    """step for splitting lists into more lists"""

    def __init__(self, compression):
        """
        :param compression: number of items per list
        """
        self.compression = compression

    def run(self, data:list)->list[list]:
        """
        splits the list into smaller lists
        :param data: list to split
        :return: list of lists
        """
        return [data[i:i + self.compression] for i in range(0, len(data), self.compression)]

    def __str__(self):
        return f"List Split -> {self.compression}"
