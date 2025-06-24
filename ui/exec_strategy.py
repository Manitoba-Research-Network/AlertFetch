from abc import ABC, abstractmethod

from lib.api import Runnable, ApiRunner


class Strategy(ABC):
    """API strategy class"""
    def __init__(self, main_runner, runner):
        """
        :param main_runner: runner for the api runner
        :param runner: ApiRunner to run with
        """
        #^ this is confusing, I'm real bad at naming things
        self.main_runner:Runnable=main_runner
        self.runner:ApiRunner=runner

    @abstractmethod
    def confirm(self):
        pass
    @abstractmethod
    def run(self):
        pass

class SingleAPIStrategy(Strategy):
    """strategy for single api"""

    def __init__(self, main_runner, runner, api):
        """
        :param main_runner: runner for the api
        :param runner: ApiRunner
        :param api: api run with
        """
        super().__init__(main_runner,runner)
        self.api=api

    def confirm(self):
        return self.runner.confirm(self.api, self.main_runner)

    def run(self):
        return self.runner.run(self.api, self.main_runner)


class AllAPIStrategy(Strategy):
    """strategy for all api's"""
    def confirm(self):
        return self.runner.confirm_all(self.main_runner)

    def run(self):
        return self.runner.run_all(self.main_runner)