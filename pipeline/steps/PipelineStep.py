from abc import abstractmethod, ABC


class PipelineStep(ABC):
    """Abstract class for pipeline steps"""
    @abstractmethod
    def run(self, data):
        """
        run the pipeline step with the data
        :param data: some kind of data the step will process, see concrete implementations for details on io to a step
        :return: some data for the next step
        """
        pass

    @abstractmethod
    def __str__(self):
        return "PipelineStep"