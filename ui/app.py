import datetime
import threading
import tkinter as tk
import traceback
from tkinter import ttk

from AlertFetcher import MainRunner
from ai.AiClient import AIClient
from lib.api import ApiRunner
from lib.retrieval import QueryOptions
from lib.runners import GroupingRunner
from ui.LabeledText import PresetText
from ui.ai_menu import AIMenu
from ui.api_selector import APISelector
from ui.confirmation import ConfirmationDialog
from ui.date_selector import DateSelector
from ui.exec_strategy import Strategy, SingleAPIStrategy, AllAPIStrategy
from ui.file_selector import FileSelector
from ui.labeled_field import LabeledSpinbox, LabeledEntry
from ui.timeframe_selector import TimeframeSelector

DEFAULT_LIMIT = 100
DEFAULT_OUT_DIR = "./out/"
DEFAULT_END_DATE = str(datetime.date.today())
DEFAULT_START_DATE = str(datetime.date.today() - datetime.timedelta(days=5))

def threaded(fn):
    def inner(self, runner):
        #threading.Thread(target=fn,args=(self,runner)).start() # this is probably a memory leak
        fn(self,runner) # todo fix this
    return inner

class App:
    """main ui class"""
    def __init__(self, api_runner:ApiRunner, config:dict, ai_client:AIClient):
        """
        :param api_runner: ApiRunner for the ui instance
        :param config: config dict
        :param ai_client: client for the ai
        """
        self.apis = api_runner.get_apis()
        self.runner = api_runner
        self.ai_client = ai_client
        self.root = tk.Tk()
        self.run_all = tk.BooleanVar()
        self.limit = tk.StringVar()
        self.out_path = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.api_selector = APISelector(self.apis)
        self.id_input:LabeledEntry|None = None
        self.id_var = tk.StringVar()
        self.index_input:LabeledEntry|None = None
        self.index_var = tk.StringVar()
        self.fields_list = config["exclude"]
        self.fields_list_include = tk.BooleanVar()
        self.context_presets = config["context_fields"]
        self.exec_state = tk.BooleanVar(value=False)
        self.prompt_list = config["prompts"]

        self.ctx_time = tk.StringVar()
        self.ctx_fields:PresetText|None = None

        self.exclude_fields:PresetText|None = None


    def start(self):
        """
        run the main loop of the app
        """
        self.root.title("AlertFetch")
        self.root.resizable(False, False)

        frame_left = tk.Frame(self.root, width=300)
        frame_left.grid(row=0, column=0, sticky="n")
        frame_right = tk.Frame(self.root, width=300)
        frame_right.grid(row=0, column=1, sticky="n")

        # ====Left====

        self.api_selector.build(frame_left)

        self.limit.set(str(DEFAULT_LIMIT))
        field_limit = LabeledSpinbox(frame_left, "Request Limit: ", self.limit)
        field_limit.pack(padx=3, pady=3, anchor="w")

        self.out_path.set(DEFAULT_OUT_DIR)
        out_file_select = FileSelector(frame_left, "Output Dir: ", self.out_path)
        out_file_select.pack(padx=3, pady=3, anchor="w")

        frame_exclude = self._create_exclusion_frame(frame_left)
        frame_exclude.pack(padx=3, pady=3, anchor="w")


        # ====Right====
        notebook = ttk.Notebook(frame_right)
        notebook.pack(fill="both", expand=True)

        frame_calendar = self._create_calendar_frame(frame_right)
        frame_grouping = self._create_grouping_frame(frame_right)
        frame_ai = AIMenu(frame_right, self.ai_client,self.prompt_list)

        notebook.add(frame_grouping, text="Grouping")
        notebook.add(frame_ai, text="AI Summarizer")
        notebook.add(frame_calendar, text="Calendar")

        # ====RUN LOOP====
        self.root.mainloop()

    def _create_calendar_frame(self, parent):
        """
        create the frame for the calendar widget tab
        :param parent: parent for the frame
        """
        frame = tk.Frame(parent)
        checkbox = tk.Checkbutton(frame, text="Run on all APIs", variable=self.run_all)
        checkbox.deselect()
        checkbox.pack(anchor="w", padx=3, pady=3)

        start_date = DateSelector(frame,"Start Date: ", self.start_date_var, initial=DEFAULT_START_DATE)
        start_date.pack(padx=3, pady=3)

        end_date = DateSelector(frame,"End Date: ", self.end_date_var, initial=DEFAULT_END_DATE)
        end_date.pack(padx=3, pady=3)

        self._make_button(frame, self._run_date_range, "Exec Date Range")

        return frame

    def _create_grouping_frame(self, parent):
        """
        create the frame for the grouping widget tab

        :param parent: parent for the frame
        """
        frame = tk.Frame(parent)

        self.id_input = LabeledEntry(frame,"Event ID: ", self.id_var)
        self.id_input.pack(padx=3, pady=3, anchor="w")
        self.index_input = LabeledEntry(frame,"Index: ", self.index_var)
        self.index_input.pack(padx=3, pady=3, anchor="w")
        ctx_window = TimeframeSelector(frame, self.ctx_time, "Context Timeframe: ")
        ctx_window.pack(padx=3, pady=3, anchor="w")

        ctx_fields = PresetText(frame,  self.context_presets, "Context Fields (comma seperated): ")
        ctx_fields.pack(padx=3, pady=3)
        self.ctx_fields = ctx_fields

        self._make_button(frame, self._run_grouping,"Exec Grouping")

        return frame

    def _make_button(self, frame, cb, text):
        button_execute = tk.Button(frame, text=text, command=cb)
        button_execute.pack(anchor="s")
        self.exec_state.trace_add( # callback for button to be disabled while queries are executing
            "write",
            lambda x, idx, mode: button_execute.configure(state=tk.DISABLED if self.exec_state.get() else tk.NORMAL))

    def _create_exclusion_frame(self, parent):
        frame = tk.Frame(parent)

        field = PresetText(frame, self.fields_list, "Fields: ")
        field.pack(anchor="w")
        self.exclude_fields = field

        include_button = tk.Checkbutton(frame, variable=self.fields_list_include, text="Include")
        include_button.pack(padx=3, pady=3,anchor="w")
        include_button.deselect()

        return frame

    def _run_date_range(self):
        main_runner = MainRunner(self._get_options(), self.out_path.get())
        if self.run_all.get():
            self._confirm_run_all(main_runner)
        else:
            self._confirm_run_one(main_runner)

    def _run_grouping(self):
        main_runner = GroupingRunner(
            self._get_options(),
            self.out_path.get(),
            self.id_var.get(),
            index=self.index_var.get(),
            context_window=int(self.ctx_time.get()),
            context_fields=self.ctx_fields.get()
        )
        self._confirm_run_one(main_runner)

    def _get_options(self):
        return QueryOptions(
            self.start_date_var.get(),
            self.end_date_var.get(),
            int(self.limit.get()),
            self.exclude_fields.get(),
            self.fields_list_include.get()
        )

    @threaded
    def _confirm_run_one(self, main_runner):
        self._confirm_then_run(SingleAPIStrategy(main_runner, self.runner, self.api_selector.get_api()))

    @threaded
    def _confirm_run_all(self, main_runner):
        self._confirm_then_run(AllAPIStrategy(main_runner, self.runner))

    def _confirm_then_run(self, strategy:Strategy):
        """
        confirm the user wants to run the query then run it
        """
        self.exec_state.set(True) # this is the only place where these are written to so no lock should be needed

        try:
            confirmation = strategy.confirm()
            if self._confirm(confirmation): # exit early if we fail to confirm
                strategy.run()
        except Exception as e:
            print("Exception occurred while running the query:", e)
            traceback.print_exc()

        self.exec_state.set(False)
    def _confirm(self, confirmation):
        confirmed = tk.BooleanVar()
        dialog = ConfirmationDialog(self.root, "Confirm Query", confirmation, confirmed)
        return dialog.out.get()


