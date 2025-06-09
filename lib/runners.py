from lib.api import Runnable
from lib.retrieval import ESQLWrapper, QueryOptions

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*,logs-*"


class GroupingRunner(Runnable):
    def __init__(self, q_options:QueryOptions,out, record_id, index=DEFAULT_INDEX_PAT ):
        self.out=out
        self.options = q_options
        self.index = index
        self.record_id = record_id

    def confirm(self, wrapper: ESQLWrapper, api_id: str) -> int:
        return 1 # todo

    def run(self, wrapper: ESQLWrapper, api_id: str):
        event = wrapper.get_event_by_id(self.record_id, self.index)
        print(event)