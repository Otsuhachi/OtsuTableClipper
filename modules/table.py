from typing import TypeGuard


def __check_single_table(data: dict) -> TypeGuard[dict[str, str]]:
    """１階層のデータテーブルか確認します。

    Args:
        data (dict): データ。

    Returns:
        TypeGuard[dict[str, str]]: １階層のデータテーブルか。
    """
    for kv in data.items():
        for s in kv:
            if type(s) is not str:
                return False
    return True


def __check_dual_table(data: dict) -> TypeGuard[dict[str, dict[str, str]]]:
    """２階層のデータテーブルか確認します。

    Args:
        data (dict): データ。

    Returns:
        TypeGuard[dict[str, str]]: ２階層のデータテーブルか。
    """
    for k, v in data.items():
        if type(k) is not str:
            return False
        if not __check_single_table(v):
            return False
    return True


def __check_triple_table(data: dict) -> TypeGuard[dict[str, dict[str, dict[str, str]]]]:
    """３階層のデータテーブルか確認します。

    Args:
        data (dict): データ。

    Returns:
        TypeGuard[dict[str, str]]: ３階層のデータテーブルか。
    """
    for k, v in data.items():
        if type(k) is not str:
            return False
        if not __check_dual_table(v):
            return False
    return True


def check_table_type(data: object) -> tuple[dict, int]:
    if not isinstance(data, dict):
        msg = f"dataはdict型として扱えません。({type(data)})"
        raise TypeError(msg)
    if __check_single_table(data):
        return data, 1
    elif __check_dual_table(data):
        return data, 2
    elif __check_triple_table(data):
        return data, 3
    msg = "dataは３階層までのdict型で、keyはstr型, valueは末端階層以外はdict型、末端階層はstr型である必要があります。"
    raise ValueError(msg)
