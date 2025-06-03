from tkinter import Frame
import tkinter as tk


class LabeledField(Frame):
    """
    Spinbox with a label
    """
    def __init__(self, parent, label_text:str, out: tk.StringVar):
        """
        :param parent: parent widget
        :param label_text: label for the field
        :param out: output Var
        """
        super().__init__(parent)
        label = tk.Label(self, text=label_text)
        label.grid(row=0, column=0)

        entry = tk.Spinbox(
            self,
            textvariable=out,
            from_=10,
            to=10000
        )
        entry.grid(row=0, column=1)