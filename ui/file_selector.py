import tkinter as tk
from tkinter import filedialog


class FileSelector(tk.Frame):
    """
    Selector for an output directory
    """
    def __init__(self, master, label_text:str, path: tk.StringVar, d_type = "dir", types = (("JSONL",".jsonl"),), start_path = "."):
        """
        :param master: parent widget
        :param label_text: label for the selector
        :param path: path output Variable
        """
        tk.Frame.__init__(self, master)
        self.path = path
        self.d_type = d_type
        self.types = types
        self.start_path = start_path

        label = tk.Label(self, text=label_text)
        label.grid(row=0, column=0)

        label_path = tk.Label(self, textvariable=path, font=("Arial", 8, "italic"))
        label_path.grid(row=0, column=1)

        button_change = tk.Button(self, text="Change", command=self._run_file_dialog)
        button_change.grid(row=1, column=0,sticky=tk.W)

    def _run_file_dialog(self):
        match self.d_type:
            case "dir":
                runner = filedialog.askdirectory
            case "ofile":
                runner = filedialog.askopenfilename
            case "sfile":
                runner = filedialog.asksaveasfilename
            case _:
                raise "invalid dialogue type"
        
        path = runner(initialdir=self.start_path, filetypes=self.types, defaultextension=self.types[0][1])
        self.path.set(path)
