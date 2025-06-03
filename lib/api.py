from abc import ABC, abstractmethod

from lib.retrieval import ESQLWrapper, QueryOptions


class Runnable(ABC):
    @abstractmethod
    def run(self, wrapper:ESQLWrapper, api_id:str):
        pass

class ApiRunner:
    def __init__(self,apis:dict):
        self.api_creds = apis
        self.apis = {}

    def get_esql_wrapper(self, api_id:str):
        """
        get the esql wrapper for an api
        :param api_id: id of the api
        """
        if api_id not in self.api_creds: # cant work with invalid ids
            raise KeyError(f"{api_id} is not a valid api id")

        if api_id not in self.apis: # lazy load
            creds = self.api_creds[api_id]
            self.apis[api_id] = ESQLWrapper(creds["uri"], creds["key"])

        return self.apis[api_id]

    def run(self, api_id:str, runnable:Runnable):
        """
        run a runnable with the given api

        :param api_id: id of the api to use
        :param runnable: what to run
        """
        wrapper = self.get_esql_wrapper(api_id)
        runnable.run(wrapper, api_id)

    def run_all(self, runnable:Runnable):
        """
        run a runnable with all apis

        :param runnable: runnable to run
        """
        for api_id in self.api_creds.keys():
            try:
                self.run(api_id, runnable)
            except Exception as e:
                print(f"{api_id} failed to run")
                print(e)

    def get_apis(self)->list:
        """
        get all api ids for this ApiRunner
        :return: list of api ids
        """
        return list(self.api_creds.keys())
