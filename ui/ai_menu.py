import tkinter as tk
from tkinter import ttk

from pipeline import *
from ui.file_selector import FileSelector
from ui.labeled_field import LabeledSpinbox, LabeledEntry

DEFAULT_PROMPTS = (
    "The following are summaries from alerts that are all related to each other, write a brief summary of these summaries",
    "The following are related events, please write a 1 paragraph summary of these events"
)

DEFAULT_INPUT_DIR = "./out/"
DEFAULT_OUTPUT_DIR = "./runs/"

class AIMenu(tk.Frame):
    """frame for ai execution menu"""

    pipeline_lut:dict[str,Callable[[AIClient, str,...],PipelineRunner]] = {
        "Multi Summary":MultiEventSummary,
        "Single Summary":MultiEventSingleSummary,
        "Intermediate":intermediate_summary
    }

    json_process_modes:list[str] = [
        AIJsonPreprocess.MODE_JSON,
        AIJsonPreprocess.MODE_NEWLINE
    ]

    def __init__(self, master, client:AIClient, prompts:list[str] = DEFAULT_PROMPTS):
        """
        :param master: parent frame
        :param client: ai client to use
        :param prompts: list of prompts to use
        """
        tk.Frame.__init__(self, master)
        self.in_file = tk.StringVar()
        self.out_file = tk.StringVar()

        self.pipeline_type = tk.StringVar()
        self.client = client

        self.prompt_list = prompts
        self.prompt = tk.StringVar()
        self.prompt.set(self.prompt_list[0])

        self.depth = tk.StringVar()
        self.depth.set("2")
        self.compress = tk.StringVar()
        self.compress.set("3,2")
        self.prompt_inter = tk.StringVar()
        self.prompt_inter.set(self.prompt_list[-1])

        self.inter_settings = None

        self.json_process_mode = tk.StringVar()
        self.json_process_mode.set(self.json_process_modes[0])

        self._build()

    def _build(self):
        in_field = FileSelector(self, "Input File: ", self.in_file, "ofile", start_path=DEFAULT_INPUT_DIR)
        in_field.pack(anchor="w", padx=3, pady=3)

        out_field = FileSelector(
            self,
            "Output File: ",
            self.out_file,
            "sfile",
            types=(("TXT", "*.txt"),),
            start_path=DEFAULT_OUTPUT_DIR)
        out_field.pack(anchor="w", padx=3, pady=3)


        mode_options = self._mode_options(self)
        mode_options.pack(anchor="w", padx=3, pady=3)

        prompt_combo = ttk.Combobox(self, textvariable=self.prompt, values=self.prompt_list)
        prompt_combo.pack(anchor="w", padx=3, pady=3)
        prompt_combo.config(width=70)

        container = ttk.Frame(self)
        inter_settings = self._intermediate_options(container)
        inter_settings.pack(anchor="w", padx=3, pady=3)
        container.pack(anchor="w", padx=3, pady=3)
        self.inter_settings = inter_settings

        exec_butt = tk.Button(self, text="Run AI", command=self._on_button)
        exec_butt.pack(anchor="w", pady=10)

        self.pipeline_type.trace_add("write", self._on_pipeline_changed)
        self._on_pipeline_changed()

    def _on_button(self):
        pipe = self.pipeline_lut[self.pipeline_type.get()](self.client, self.prompt.get(),**self._make_kwargs())
        if self.out_file.get():
            pipe.add_step(WriteData(self.out_file.get()))
        print(pipe.execute(self.in_file.get()))

    def _mode_options(self, parent):
        frame = tk.Frame(parent)
        tk.Label(frame, text="Text Mode:").grid(row=0, column=0, padx=3, pady=3,sticky="e")
        pre_process_drop = ttk.OptionMenu(frame, self.json_process_mode, self.json_process_modes[0], *self.json_process_modes)
        pre_process_drop.grid(row=0, column=1, padx=3, pady=3)
        pre_process_drop.config(width=20)

        tk.Label(frame, text="Process Mode:").grid(row=1, column=0, padx=3, pady=3,sticky="e")
        drop = ttk.OptionMenu(frame, self.pipeline_type, list(self.pipeline_lut.keys())[0], *self.pipeline_lut.keys())
        drop.grid(row=1, column=1, padx=3, pady=3)
        drop.config(width=20)


        return frame

    def _intermediate_options(self, parent):
        frame = tk.Frame(parent)
        depth_field = LabeledSpinbox(frame, "Depth: ", self.depth, _from=0, to=10)
        depth_field.grid(row=0, column=0, sticky="w")

        compress_field = LabeledEntry(frame, "Compression: ", self.compress)
        compress_field.grid(row=0, column=1, sticky="w")

        prompt_combo = ttk.Combobox(frame, textvariable=self.prompt_inter, values=self.prompt_list)
        prompt_combo.grid(row=1, column=0, sticky="w", columnspan=2)
        prompt_combo.config(width=70)

        return frame

    def _on_pipeline_changed(self, *_):
        if self.pipeline_type.get() == "Intermediate":
            self.inter_settings.pack()
        else:
            self.inter_settings.pack_forget()

    def _make_kwargs(self):
        return {
            "depth": int(self.depth.get()),
            "compression": [int(i) for i in self.compress.get().split(",")],
            "prompt_intermediate": self.prompt_inter.get(),
            "mode": self.json_process_mode.get()
        }








