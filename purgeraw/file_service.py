from typing import Tuple, Callable


def fake_delete(path: str) -> bool:
    pass


def delete(path: str) -> bool:
    pass


def raw_determinator(raw_exts: Tuple[str], processed_exts: Tuple[str]) -> Callable[[str], bool]:

    def is_raw(path: str) -> bool:
        pass

    return is_raw
