import tkinter as tk
from tkinter import filedialog


class FileSelector(tk.Frame):
    def __init__(self, master, label_text:str, path: tk.StringVar):
        tk.Frame.__init__(self, master)
        self.path = path

        label = tk.Label(self, text=label_text)
        label.grid(row=0, column=0)

        label_path = tk.Label(self, textvariable=path, font=("Arial", 8, "italic"))
        label_path.grid(row=0, column=1)

        button_change = tk.Button(self, text="Change", command=self._run_file_dialog)
        button_change.grid(row=1, column=0,sticky=tk.W)

    def _run_file_dialog(self):
        path = filedialog.askdirectory(initialdir=".")
        self.path.set(path)
