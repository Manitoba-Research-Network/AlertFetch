import tkinter as tk
from tkinter import ttk

class LabeledText(tk.Frame):
    """
    class for a labeled text box
    """
    def __init__(self, master, label_text:str):
        tk.Frame.__init__(self, master)

        label = tk.Label(self, text=label_text)
        label.pack(anchor="w")

        textbox = tk.Text(self, height=5, width=60)
        textbox.pack(anchor="w")
        textbox.config()
        self.textbox = textbox

    def get(self)->str:
        """
        get the string value in the textbox
        """
        return self.textbox.get("1.0", tk.END)



class PresetText(tk.Frame):
    """text box with a dropdown for presets"""
    def __init__(self, parent, presets:dict[str,str], label_text:str):
        """
        :param parent: parent frame
        :param presets: dict of presets {"name":"preset text"}
        :param label_text: label for the box
        """
        tk.Frame.__init__(self, parent)
        self.presets = presets


        self.preset_var = tk.StringVar()
        preset_menu = self._create_preset_menu(label_text)
        preset_menu.pack(anchor="w")

        textbox = tk.Text(self, height=5, width=60)
        textbox.pack(anchor="w")
        textbox.config()
        self.textbox = textbox

        self._on_preset_changed(self.preset_var)

    def _create_preset_menu(self, label_text:str):
        frame = tk.Frame(self)
        label = tk.Label(frame, text=label_text)
        label.grid(row=0, column=0)
        option = ttk.OptionMenu(frame, self.preset_var, list(self.presets.keys())[0], *self.presets.keys(), command=self._on_preset_changed)
        option.grid(row=0, column=1)
        return frame

    def _on_preset_changed(self, _):
        preset = ','.join(self.presets[self.preset_var.get()])
        self.textbox.delete('1.0',tk.END)
        self.textbox.insert('1.0', preset)


    def get(self)->list[str]:
        return [e.strip() for e in self.textbox.get("1.0", tk.END).split(',')]




