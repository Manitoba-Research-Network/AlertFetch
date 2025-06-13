import tkinter as tk
from tkinter import ttk

from pipeline import *
from ui.file_selector import FileSelector

DEFAULT_PROMPTS = [
    "The following are related events, please write a 1 paragraph summary of these events"
] # todo add this dropdown

class AIMenu(tk.Frame):

    pipeline_lut:dict[str,Callable[[AIClient, str],PipelineRunner]] = {
        "Single Summary":MultiEventSingleSummary,
        "Multi Summary":MultiEventSummary
    }

    def __init__(self, master, client:AIClient):
        tk.Frame.__init__(self, master)
        self.in_file = tk.StringVar()
        self.out_file = tk.StringVar()

        self.pipeline_type = tk.StringVar()
        self.client = client

        self.prompt = tk.StringVar()
        self.prompt.set(DEFAULT_PROMPTS[0])

        self._build()

    def _build(self):
        in_field = FileSelector(self, "Input File: ", self.in_file, "ofile")
        in_field.pack(anchor="w", padx=3, pady=3)

        out_field = FileSelector(self, "Output File: ", self.out_file, "sfile")
        out_field.pack(anchor="w", padx=3, pady=3)

        drop = ttk.OptionMenu(self, self.pipeline_type, list(self.pipeline_lut.keys())[0], *self.pipeline_lut.keys())
        drop.pack(anchor="w", padx=3, pady=3)
        drop.config(width=20)

        exec_butt = tk.Button(self, text="Run AI", command=self._on_button)
        exec_butt.pack(anchor="w", pady=10)

    def _on_button(self):
        pipe = self.pipeline_lut[self.pipeline_type.get()](self.client, self.prompt.get())
        print(pipe.execute(self.in_file.get()))








