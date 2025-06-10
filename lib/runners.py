from lib.api import Runnable
from lib.output import write_jsonl, write_jsonl_no_label
from lib.processing import clean_entries
from lib.retrieval import ESQLWrapper, QueryOptions

DEFAULT_INDEX_PAT = ".internal.alerts-security.alerts-default-*,logs-*"


class GroupingRunner(Runnable):
    def __init__(self, q_options:QueryOptions,out, record_id, context_fields:list, context_window:int, index=DEFAULT_INDEX_PAT):
        self.out=out
        self.options = q_options
        self.index = index
        self.record_id = record_id
        self.ctx_fields = context_fields
        self.ctx_window = context_window

        self._event = None

    def confirm(self, wrapper: ESQLWrapper, api_id: str) -> int:
        print(f"[Counting] {self}")

        # * get event from id
        event = self._get_event(wrapper)

        # * count context events
        fields = self._zip_fields(event)

        return wrapper.count_ctx(fields, self.ctx_window, event["@timestamp"],self.index)

    def _zip_fields(self, event):
        fields = {}
        for field in self.ctx_fields:
            try:
                field_value = event[field]
            except KeyError:
                field_value = None

            if field_value is None: # skip field if not found in progenitor event
                print(f"Field {field} not found in event")
                continue
            fields[field] = field_value
        return fields

    def run(self, wrapper: ESQLWrapper, api_id: str):
        print(f"[Running] {self}")
        # * get event from id
        event = self._get_event(wrapper)

        # * get context events
        fields = self._zip_fields(event)

        res =  wrapper.get_ctx(fields, self.ctx_window, event["@timestamp"],self.index, self.options)

        # clean
        cleaned = clean_entries(res, api_id)

        # write out
        write_jsonl_no_label(self.out + f"{api_id}.jsonl", cleaned)





    def _get_event(self, wrapper: ESQLWrapper):
        if self._event is None:
            self._event = wrapper.get_event_by_id(self.record_id, self.index)
        return self._event

    def __str__(self):
        return f"GroupingRunner -> window:{self.ctx_window}, fields:{self.ctx_fields}, index:{self.index}"