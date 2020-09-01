from typing import List, Callable


def purger(walker: Callable[[str], List[str]],
           deleter: Callable[[str], None],
           raw_determinator: Callable[[str], bool]
           ) -> Callable[[str], None]:

    def purge(input_dir: str) -> None:
        print(f"Purging: {input_dir}")
        files = walker(input_dir)

    return purge
