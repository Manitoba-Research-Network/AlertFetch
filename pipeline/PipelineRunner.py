from pipeline.steps.PipelineStep import PipelineStep

class PipelineRunner:
    def __init__(self, name):
        self.steps:list[PipelineStep] = []
        self.name = name

    def add_step(self, step:PipelineStep):
        self.steps.append(step)
        return self

    def execute(self, start_data):
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
        for step in self.steps:
            print(f"[{self}] -> {step}")