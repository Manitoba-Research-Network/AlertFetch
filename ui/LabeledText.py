import tkinter as tk

class LabeledText(tk.Frame):
    def __init__(self, master, label_text:str):
        tk.Frame.__init__(self, master)

        label = tk.Label(self, text=label_text)
        label.pack(anchor="w")

        textbox = tk.Text(self, height=5, width=60)
        textbox.pack(anchor="w")
        textbox.config()
        self.textbox = textbox

    def get(self)->str:
        return self.textbox.get("1.0", tk.END)






