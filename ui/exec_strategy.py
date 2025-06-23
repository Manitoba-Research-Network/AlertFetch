from abc import ABC, abstractmethod

from lib.api import Runnable, ApiRunner


class Strategy(ABC):
    def __init__(self, main_runner, runner):
        self.main_runner:Runnable=main_runner
        self.runner:ApiRunner=runner

    @abstractmethod
    def confirm(self):
        pass
    @abstractmethod
    def run(self):
        pass

class SingleAPIStrategy(Strategy):

    def __init__(self, main_runner, runner, api):
        super().__init__(main_runner,runner)
        self.api=api

    def confirm(self):
        return self.runner.confirm(self.api, self.main_runner)

    def run(self):
        return self.runner.run(self.api, self.main_runner)


class AllAPIStrategy(Strategy):
    def confirm(self):
        return self.runner.confirm_all(self.main_runner)

    def run(self):
        return self.runner.run_all(self.main_runner)