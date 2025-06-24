from pipeline.steps.PipelineStep import PipelineStep

class PipelineRunner:
    """Runs pipeline steps"""
    def __init__(self, name):
        """
        :param name: name of the pipeline
        """
        self.steps:list[PipelineStep] = []
        self.name = name

    def add_step(self, step:PipelineStep):
        """
        add a step to the pipeline
        :param step: step to add
        """
        self.steps.append(step)
        return self

    def execute(self, start_data):
        """
        execute the pipeline
        :param start_data: initial data to send to the pipeline
        :return: pipeline result
        """
        data = start_data
        print(f"{self} Running...")

        for step in self.steps:
            print(f"[{self}] -> {step}")
            data = step.run(data)

        print(f"{self} Finished!")
        return data

    def __str__(self):
        return self.name

    def print_steps(self):
        """
        print the steps for this pipeline
        """
        for step in self.steps:
            print(f"[{self}] -> {step}")