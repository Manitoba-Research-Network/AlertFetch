from lib.api import Runnable
from lib.retrieval import ESQLWrapper, QueryOptions

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*,logs-*"


class GroupingRunner(Runnable):
    def __init__(self, q_options:QueryOptions,out, record_id, context_fields:list, context_window:int, index=DEFAULT_INDEX_PAT):
        self.out=out
        self.options = q_options
        self.index = index
        self.record_id = record_id
        self.ctx_fields = context_fields
        self.context_window = context_window

    def confirm(self, wrapper: ESQLWrapper, api_id: str) -> int:
        print(f"[Counting] {self}")
        # * get events from id
        # todo
        # * count context events
        # todo
        return 1 # todo

    def run(self, wrapper: ESQLWrapper, api_id: str):
        print("[Running] {self}")
        # * get event from id
        event = wrapper.get_event_by_id(self.record_id, self.index)
        print(event)
        # * get context events

    def __str__(self):
        return f"GroupingRunner -> window:{self.context_window}, fields:{self.ctx_fields}, index:{self.index}"