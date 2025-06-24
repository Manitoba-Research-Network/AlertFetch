import tkinter as tk
from tkinter import ttk

from ui.labeled_field import LabeledSpinbox

time_lut = {
    "min":60,
    "sec":1,
    "hrs":3600
}

class TimeframeSelector(tk.Frame):
    """
    selector for a time and units for the time
    """
    def __init__(self, parent, out: tk.StringVar, label_text: str):
        """
        :param parent: parent frame
        :param out: output var, outputs in seconds
        :param label_text: label for the field
        """
        tk.Frame.__init__(self, parent)
        self.out = out

        self.spin_var = tk.StringVar()
        spin = LabeledSpinbox(self, label_text, self.spin_var)
        spin.grid(column=0, row=0)

        self.time_var = tk.StringVar()
        option = ttk.OptionMenu(self, self.time_var, list(time_lut.keys())[0], *time_lut.keys())
        option.grid(column=1, row=0)
        option.config(width=10)

        self.spin_var.trace_add("write", self._on_change)
        self.time_var.trace_add("write", self._on_change)
        self._on_change() # ! force initial state

    def _on_change(self, *args):
        self.out.set(str(
            time_lut[self.time_var.get()] * int(self.spin_var.get())
        ))
