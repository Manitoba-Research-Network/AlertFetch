import tkinter as tk

from ui.api_selector import APISelector


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

        button_execute = tk.Button(frame_left, text="Execute", command=lambda: print(api_selector.get_api()))
        button_execute.pack()

        root.mainloop()
