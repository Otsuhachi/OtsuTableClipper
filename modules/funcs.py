import os
import sys
import tkinter.messagebox as tkm
import tkinter.ttk as ttk

from functools import wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

import pyperclip

from otsutil import OtsuNone, load_json, pathLike, str_to_path

from .table import check_table_type

__P = ParamSpec("__P")
__R = TypeVar("__R")
__RUNNING_FUNCS = []


def beep() -> None:
    try:
        import winsound

        freq = 1500
        dur = 200
        winsound.Beep(freq, dur)
    except:
        pass


def clip(text: str) -> None:
    """クリップボードにtextを登録します。

    Args:
        text (str): 登録する文字列。
    """
    pyperclip.copy(text)


def close_std(func: Callable[__P, __R]) -> Callable[__P, __R]:
    """標準出力, 標準エラーを閉鎖します。

    __RUNNING_FUNCSが空になったとき、閉鎖を解除します。

    Args:
        func (Callable[__P, __R]): 閉鎖中に実行する関数。

    Returns:
        Callable[__P, __R]: 閉鎖中に実行する関数。
    """

    @wraps(func)
    def __inner(*args: __P.args, **kwargs: __P.kwargs) -> __R:
        if not __RUNNING_FUNCS:
            sys.stdout = open(os.devnull, "w")
            sys.stderr = open(os.devnull, "w")
        __RUNNING_FUNCS.append(1)
        res = func(*args, **kwargs)
        __RUNNING_FUNCS.pop()
        if not __RUNNING_FUNCS:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
        return res

    return __inner


def copy_data(cmb: ttk.Combobox, data: dict[str, str]) -> None:
    """Comboboxで選択された項目に応じてクリップボードに文字列を登録します。

    Args:
        combo (ttk.Combobox): Combobox。
        data (dict[str, str]): "項目名", "コピーする文字列"の辞書。
    """
    selected_name = cmb.get()
    value = data.get(selected_name, OtsuNone)
    if type(value) is not str:
        title = "選択されたコマンドは登録されていません。"
        msg = "処理を実行できませんでした。"
        tkm.showerror(title, msg)
        return
    clip(value)
    beep()


def load_data(path: Path) -> tuple[dict, int]:
    if not path.is_file():
        msg = f"{path.resolve()}は存在しないかフォルダです。"
        raise FileNotFoundError(msg)
    data = load_json(path)
    return check_table_type(data)


def resolve_meipass(path: pathLike) -> Path:
    """スクリプトを実行したときと、Exe化しているときでPathが異なるファイルの読込を解決します。

    存在するファイル専用の関数です。

    Args:
        path (pathLike): 読み込むファイルのパス。

    Raises:
        TypeError: sys._MEIPASSが存在するがstr型では無かった場合に投げられます。
        FileNotFoundError: パスが存在しなかった場合に投げられます。

    Returns:
        Path: 場所の解決されたPath。
    """
    if (meipass := getattr(sys, "_MEIPASS", OtsuNone)) is OtsuNone:
        res = str_to_path(path)
    elif type(meipass) is not str:
        msg = f"_MEIPASSを正常に取得できませんでした。({meipass=})"
        raise TypeError(msg)
    else:
        res = str_to_path(meipass) / path
    if not res.exists():
        msg = f"{res.resolve()}は存在しません。"
        raise FileNotFoundError(msg)
    return res


def show_exception(E: Exception) -> None:
    """例外発生のメッセージウィンドウを表示します。

    Args:
        E (Exception): 例外。
    """
    title = f"{type(E)}が発生したためプログラムが強制終了しました"
    msg = f"{E}"
    tkm.showerror(title, msg)
