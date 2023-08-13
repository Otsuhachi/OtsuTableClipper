import tkinter as tk
import tkinter.ttk as ttk

from abc import ABC, abstractmethod

from otsutil import OtsuNone

from modules import copy_data


class __TableClipper(tk.Frame, ABC):
    def __init__(self, data: dict, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.set_widgets(data)

    @abstractmethod
    def set_widgets(self, data: dict) -> None:
        ...


class SingleTC(__TableClipper):
    def set_widgets(self, data: dict[str, str]) -> None:
        self.__data = data
        cmb = ttk.Combobox(self, values=list(data.keys()), width=45)
        cmb.current(0)
        btn = ttk.Button(
            self,
            text="コピー",
            command=lambda combo=cmb, data=data: copy_data(combo, data),
        )
        cmb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        btn.pack(side=tk.LEFT, padx=10)


class DualTC(__TableClipper):
    def __on_change(self, _=None) -> None:
        key = self.__combo.get()
        data = self.__data
        value = data.get(key, OtsuNone)
        if not isinstance(value, dict):
            return
        self.__fr_in.destroy()
        self.__fr_in = SingleTC(value, self.__fr_bottom)
        self.__fr_in.pack(fill=tk.BOTH, expand=True)

    def set_widgets(self, data: dict[str, dict[str, str]]) -> None:
        self.__data = data
        self.fr_top = top = tk.Frame(self)
        self.__fr_bottom = bottom = tk.Frame(self)
        self.__fr_in = tk.Frame(bottom)
        self.__combo = cmb = ttk.Combobox(top, values=list(data.keys()), width=45)
        cmb.current(0)
        self.__on_change()
        cmb.bind("<<ComboboxSelected>>", self.__on_change)
        cmb.pack(fill=tk.X)
        bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=10)
        self.__fr_in.pack(fill=tk.BOTH, expand=True)
        top.pack(side=tk.BOTTOM, fill=tk.X, pady=10)


class TripleTC(__TableClipper):
    def set_widgets(self, data: dict[str, dict[str, dict[str, str]]]) -> None:
        self.__note = note = ttk.Notebook(self)
        for k, v in data.items():
            note.add(DualTC(v, note), text=k)
        note.pack(fill=tk.BOTH, expand=True)
