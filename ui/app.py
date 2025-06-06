import datetime
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

import lib.output
from AlertFetcher import MainRunner
from lib.api import ApiRunner
from lib.retrieval import QueryOptions
from ui.api_selector import APISelector
from ui.confirmation import ConfirmationDialog
from ui.date_selector import DateSelector
from ui.file_selector import FileSelector
from ui.labeled_field import LabeledSpinbox, LabeledEntry
from ui.mode_selector import ModeSelector

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
        self.mode_selector = None
        self.id_input:LabeledEntry|None = None
        self.id_var = tk.StringVar()
        self.blacklist = blacklist
        self.exec_state = tk.BooleanVar(value=False)


    def start(self):
        """
        run the main loop of the app
        """
        self.root.title("AlertFetch")
        self.root.resizable(False, False)

        frame_left = tk.Frame(self.root, width=300)
        frame_left.grid(row=0, column=0, sticky="n")
        frame_right = tk.Frame(self.root, width=300)
        frame_right.grid(row=0, column=1)

        # ====Left====
        self.mode_selector = ModeSelector(frame_left, self._on_mode_select)
        self.mode_selector.pack(padx=3, pady=3, anchor="w")

        self.api_selector.build(frame_left)

        self.id_input = LabeledEntry(frame_left,"Event ID: ", self.id_var)
        self.id_input.pack(padx=3, pady=3, anchor="w")

        self.limit.set(str(DEFAULT_LIMIT))
        field_limit = LabeledSpinbox(frame_left, "Request Limit: ", self.limit)
        field_limit.pack(padx=3, pady=3)

        self.out_path.set(DEFAULT_OUT_DIR)
        out_file_select = FileSelector(frame_left, "Output Dir: ", self.out_path)
        out_file_select.pack(padx=3, pady=3, anchor="w")

        button_execute = tk.Button(frame_left, text="Execute", command=self._on_button)
        button_execute.pack()
        self.exec_state.trace_add( # calback for button to be disabled while queries are executing
            "write",
            lambda x, idx, mode: button_execute.configure(state=tk.DISABLED if self.exec_state.get() else tk.NORMAL))

        # ====Right====
        notebook = ttk.Notebook(frame_right)
        notebook.pack(fill="both", expand=True)

        # Calendars
        frame_calendar = self._create_calendar_frame(frame_right)

        notebook.add(frame_calendar, text="Date Range")

        # ====INIT STATE====
        self._on_mode_select(self.mode_selector.get_value())

        # ====RUN LOOP====
        self.root.mainloop()

    def _create_calendar_frame(self, parent):
        frame = tk.Frame(parent)

        start_date = DateSelector(frame,"Start Date: ", self.start_date_var, initial=DEFAULT_START_DATE)
        start_date.pack(padx=3, pady=3)

        end_date = DateSelector(frame,"End Date: ", self.end_date_var, initial=DEFAULT_END_DATE)
        end_date.pack(padx=3, pady=3)


        return frame

    def _on_mode_select(self, mode):
        match mode:
            case "single":
                self.id_input.set_enabled(True)
                self.api_selector.disable_multi()
            case "multi":
                self.id_input.set_enabled(False)
                self.api_selector.enable_multi()

    def _on_button(self): # button event handler
        threading.Thread(target=self._confirm_then_run()).start() # this is probably a memory leak

    def _confirm_then_run(self):
        self.exec_state.set(True) # this is the only place where these are written to so no lock should be needed

        options = QueryOptions(self.start_date_var.get(), self.end_date_var.get(), int(self.limit.get()), self.blacklist)
        main_runner = MainRunner(options, self.out_path.get())
        api = self.api_selector.get_api()

        ## RUN CONFIRMATION
        if api != "ALL":
            confirmation = self.runner.confirm(api, main_runner)
            pass # count for all
        else:
            confirmation = self.runner.confirm_all(main_runner)
            pass # count for one

        confirmed = tk.BooleanVar()
        ConfirmationDialog(self.root, "Confirm Query", confirmation, confirmed)

        ## RUN FETCH
        if confirmed.get(): # exit early if we fail to confirm
            if api != "ALL": # check if we are running for all apis
                self.runner.run(api, main_runner)
            else:
                self.runner.run_all(main_runner)
                lib.output.combine_jsonl(self.out_path.get())

        self.exec_state.set(False)


