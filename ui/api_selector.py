from tkinter import Frame, StringVar
from tkinter import ttk


class APISelector:
    """
    UI for selecting api(s) to query.
    """
    def __init__(self, apis):
        """
        :param apis: list of api ids
        """
        self.apis = apis
        self.selected_api = StringVar()
        self.dropdown:ttk.OptionMenu = None

    def build(self, parent):
        """
        builds the ui component

        :param parent: parent widget
        :return:
        """
        frame = Frame(parent)
        frame.pack(fill="x", padx=3, pady=3, expand=True)

        label = ttk.Label(frame, text= "API:")
        label.grid(column=0, row=0)

        dropdown = ttk.OptionMenu(
            frame,
            self.selected_api,
            self.apis[0] if len(self.apis) > 0 else "NO APIS",
            *self.apis,
            command=self._on_selected_change)
        dropdown.config(width=20)
        dropdown.grid(column=1, row=0)
        self.dropdown = dropdown


    def _on_selected_change(self, selected):
        self.selected_api.set(selected)

    def get_api(self):
        """
        get the selected api
        :return: string id of the selected api ('ALL' if all selected)
        """
        return self.selected_api.get()
