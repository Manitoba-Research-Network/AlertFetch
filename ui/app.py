import tkinter as tk

from ui.api_selector import APISelector
from ui.file_selector import FileSelector
from ui.labeled_field import LabeledField

DEFAULT_LIMIT = 100
DEFAULT_OUT_DIR = "./out"


class App:
    def __init__(self, apis):
        self.apis = apis

    def start(self):
        root = tk.Tk()
        root.title("AlertFetch")
        root.resizable(False, False)

        frame_left = tk.Frame(root, width=300, bg="skyblue")
        frame_left.grid(row=0, column=0)
        frame_right = tk.Frame(root, width=300, bg="green")
        frame_right.grid(row=0, column=1)

        # Left
        api_selector = APISelector(self.apis)
        api_selector.build(frame_left)

        limit = tk.StringVar(value=str(100))
        field_limit = LabeledField(frame_left,"Request Limit: ", limit)
        field_limit.pack(padx=3, pady=3)

        out_path = tk.StringVar(value=DEFAULT_OUT_DIR)
        out_file_select = FileSelector(frame_left, "Output Dir: ", out_path)
        out_file_select.pack(padx=3, pady=3)

        button_execute = tk.Button(frame_left, text="Execute", command=lambda: print(api_selector.get_api()))
        button_execute.pack()

        root.mainloop()
