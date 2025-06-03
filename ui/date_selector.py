import datetime
import tkinter as tk
from tkinter import StringVar
import tkcalendar


class DateSelector(tk.Frame):
    def __init__(self, master, label_text:str, value:StringVar, initial:str = str(datetime.date.today())):
        """
        :param master: parent widget
        :param label_text: label for the selector
        :param value: value output Var
        :param initial: initial value
        """
        tk.Frame.__init__(self, master)
        self.value = value
        self.date_value = StringVar(value=initial)
        self.time_value = StringVar(value="00:00")

        label = tk.Label(self, text=label_text)
        label.grid(row=0, column=0)

        label_date = tk.Label(self, textvariable=self.value, font=("Arial", 8, "italic"))
        label_date.grid(row=0, column=1)

        calendar = tkcalendar.Calendar(
            self,
            textvariable=self.date_value,
            date_pattern='yyyy-mm-dd'
        )
        calendar.bind("<<CalendarSelected>>", self._on_change)
        calendar.grid(row=1, column=0, columnspan=2)
        #todo, time selector see #8

        self._on_change(None)

    def _on_change(self, _):
        self.value.set(f"{self.date_value.get()}T{self.time_value.get()}")




