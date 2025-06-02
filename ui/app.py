import datetime
import tkinter as tk

import lib.output
from AlertFetcher import MainRunner
from lib.api import ApiRunner
from lib.retrieval import QueryOptions
from ui.api_selector import APISelector
from ui.date_selector import DateSelector
from ui.file_selector import FileSelector
from ui.labeled_field import LabeledField

DEFAULT_LIMIT = 100
DEFAULT_OUT_DIR = "./out/"
DEFAULT_END_DATE = str(datetime.date.today())
DEFAULT_START_DATE = str(datetime.date.today() - datetime.timedelta(days=5))


class App:
    def __init__(self, api_runner:ApiRunner, blacklist:list):
        self.apis = api_runner.get_apis()
        self.runner = api_runner
        self.root = tk.Tk()
        self.limit = tk.StringVar()
        self.out_path = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.api_selector = APISelector(self.apis)
        self.blacklist = blacklist

    def start(self):
        self.root.title("AlertFetch")
        self.root.resizable(False, False)

        frame_left = tk.Frame(self.root, width=300, bg="skyblue")
        frame_left.grid(row=0, column=0, sticky="n")
        frame_right = tk.Frame(self.root, width=300, bg="green")
        frame_right.grid(row=0, column=1)

        # Left
        self.api_selector.build(frame_left)

        self.limit.set(str(DEFAULT_LIMIT))
        field_limit = LabeledField(frame_left,"Request Limit: ", self.limit)
        field_limit.pack(padx=3, pady=3)

        self.out_path.set(DEFAULT_OUT_DIR)
        out_file_select = FileSelector(frame_left, "Output Dir: ", self.out_path)
        out_file_select.pack(padx=3, pady=3)

        button_execute = tk.Button(frame_left, text="Execute", command=self._on_button)
        button_execute.pack()

        # Right
        start_date = DateSelector(frame_right,"Start Date: ", self.start_date_var, initial=DEFAULT_START_DATE)
        start_date.pack(padx=3, pady=3)

        end_date = DateSelector(frame_right,"End Date: ", self.end_date_var, initial=DEFAULT_END_DATE)
        end_date.pack(padx=3, pady=3)

        self.root.mainloop()

    def _on_button(self):
        options = QueryOptions(self.start_date_var.get(), self.end_date_var.get(), int(self.limit.get()), self.blacklist)
        main_runner = MainRunner(options, self.out_path.get())

        api = self.api_selector.get_api()
        if api != "ALL":
            self.runner.run(api, main_runner)
            lib.output.combine_jsonl(self.out_path.get())
        else:
            self.runner.run_all(main_runner)

