from tkinter import simpledialog
import tkinter as tk


class ConfirmationDialog(simpledialog.Dialog):
    def __init__(self, parent, title, q_text:str, out:tk.BooleanVar):
        """
        :param parent: parent widget
        :param title: title of the dialog box
        :param q_text: text in the box
        :param callback: called if OK is clicked
        """
        self.q_text = q_text
        self.out = out

        super().__init__(parent, title)# this call needs to happen last as it is blocking

    def body(self, master):
        tk.Label(master, text=self.q_text).pack()

    def apply(self):
        self.out.set(True)