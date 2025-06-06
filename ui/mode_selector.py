import tkinter as tk
from tkinter import ttk

class ModeSelector(tk.Frame):
    def __init__(self, master, command):
        tk.Frame.__init__(self, master)

        self.command = command
        self._raw_var = tk.StringVar()
        self.mode_lut = {
            "Single Event":"single",
            "Multi Event":"multi"
        }

        label = tk.Label(self, text="Mode")
        label.grid(row=0, column=0)
        option = ttk.OptionMenu(
            self,
            self._raw_var,
            list(self.mode_lut.keys())[0],
            *self.mode_lut.keys(),
            command=self._on_command
        )
        option.grid(row=0, column=1)
        option.config(width=20)



    def get_value(self):
        return self.mode_lut[self._raw_var.get()]

    def _on_command(self, _):
        self.command(self.get_value())
