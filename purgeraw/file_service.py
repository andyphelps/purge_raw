import os
from typing import List, Callable


def fake_delete(path: str) -> None:
    print(f"DRYRUN: Deleted {path}")


def delete(path: str) -> None:
    os.remove(path)


def raw_determinator(raw_exts: List[str]) -> Callable[[str], bool]:

    def is_raw(path: str) -> bool:
        path_ext = os.path.splitext(path)[1].strip(".")
        return any((path_ext == ext for ext in raw_exts))

    return is_raw
