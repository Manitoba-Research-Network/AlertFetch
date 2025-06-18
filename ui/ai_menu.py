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

    pipeline_lut:dict[str,Callable[[AIClient, str,...],PipelineRunner]] = {
        "Multi Summary":MultiEventSummary,
        "Single Summary":MultiEventSingleSummary,
        "Intermediate":intermediate_summary
    }

    def __init__(self, master, client:AIClient, prompts:list[str] = DEFAULT_PROMPTS):
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

        drop = ttk.OptionMenu(self, self.pipeline_type, list(self.pipeline_lut.keys())[0], *self.pipeline_lut.keys())
        drop.pack(anchor="w", padx=3, pady=3)
        drop.config(width=20)

        prompt_combo = ttk.Combobox(self, textvariable=self.prompt, values=self.prompt_list)
        prompt_combo.pack(anchor="w", padx=3, pady=3)
        prompt_combo.config(width=70)

        inter_settings = self._intermediate_options(self)
        inter_settings.pack(anchor="w", padx=3, pady=3)

        exec_butt = tk.Button(self, text="Run AI", command=self._on_button)
        exec_butt.pack(anchor="w", pady=10)

    def _on_button(self):
        pipe = self.pipeline_lut[self.pipeline_type.get()](self.client, self.prompt.get(),**self._make_kwargs())
        if self.out_file.get():
            pipe.add_step(WriteData(self.out_file.get()))
        print(pipe.execute(self.in_file.get()))

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

    def _make_kwargs(self):
        return {
            "depth": int(self.depth.get()),
            "compression": [int(i) for i in self.compress.get().split(",")],
            "prompt_intermediate": self.prompt_inter.get(),
        }








