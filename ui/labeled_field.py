from tkinter import Frame
import tkinter as tk

class LabeledField(Frame):
    def __init__(self, master, label_text:str, field_class, **kwargs):
        Frame.__init__(self, master)

        label = tk.Label(self, text=label_text)
        label.grid(row=0, column=0)

        self.entry = field_class(self, **kwargs)
        self.entry.grid(row=0, column=1)

    def set_enabled(self, enable:bool):
        self.entry.config(state="normal" if enable else "disabled")


class LabeledSpinbox(LabeledField):
    """
    Spinbox with a label
    """
    def __init__(self, parent, label_text:str, out: tk.StringVar):
        """
        :param parent: parent widget
        :param label_text: label for the field
        :param out: output Var
        """
        super().__init__(parent, label_text, tk.Spinbox,
                         textvariable=out,
                         from_=10,
                         to=10000
                         )

class LabeledEntry(LabeledField):
    def __init__(self, parent, label_text:str, out: tk.StringVar):
        """
        :param parent: parent widget
        :param label_text: label for the field
        :param out: output Var
        """
        super().__init__(parent, label_text, tk.Entry,
                         textvariable=out
                         )