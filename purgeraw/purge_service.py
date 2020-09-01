from itertools import chain
from typing import List, Callable, Dict, Tuple


def purger(walker: Callable[[str], List[str]],
           deleter: Callable[[str], None],
           is_raw: Callable[[str], bool],
           indexes: Callable[[str], List[Tuple[str, str]]]
           ) -> Callable[[str], None]:
    def purge(input_dir: str) -> None:
        print(f"\nPurging: {input_dir}")

        files: List[str] = walker(input_dir)
        print(f"Found {len(files)} files to process")

        raw_files: Dict[str, str] = dict([indexes(file)[0] for file in files if is_raw(file)])
        print(f"Found {len(raw_files)} raw files: {raw_files.values()}")

        processed_files: Dict[str, str] = dict(
            chain.from_iterable([indexes(file) for file in files if not is_raw(file)]))
        print(f"Found {len(processed_files)} processed files: {processed_files}")

        to_remove: List[str] = [raw_files[raw_index] for raw_index in raw_files.keys() if
                                raw_index not in processed_files.keys()]
        to_remove.sort()

        print(f"Found {len(to_remove)} files to remove: {to_remove}")

        for file in to_remove:
            deleter(file)

    return purge
