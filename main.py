import tkinter as tk

from modules import DualTC, SingleTC, TripleTC, close_std, load_data, resolve_meipass


@close_std
def main() -> None:
    pd_internal = resolve_meipass("InternalData")
    pf_project = pd_internal / "ProjectData.json"
    pf_table = pd_internal / "Table.json"
    data_project, _ = load_data(pf_project)
    project_name = data_project["NAME"]
    project_version = data_project["VERSION"]
    del data_project
    data_table, table_type = load_data(pf_table)
    root = tk.Tk()
    root.title(f"{project_name} - Ver.{project_version}")
    match table_type:
        case 1:
            app = SingleTC
        case 2:
            app = DualTC
        case 3:
            app = TripleTC
        case _:
            msg = f"未知のテーブル形式です。{table_type}"
            raise ValueError(msg)
    app(data_table, root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
