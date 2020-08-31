import os
from typing import Callable, List


def directory_walker(exts: List[str]) -> Callable[[str], List[str]]:

    def walk(directory: str) -> List[str]:
        chosen = []

        for root, dirs, files in os.walk(directory):
            chosen += [os.path.join(root, file) for file in files if any(map(file.lower().endswith, exts))]

        return chosen

    return walk
