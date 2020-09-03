from typing import Tuple

import click
from toolz import pipe  # type: ignore

from purgeraw import __version__
from purgeraw.directory_walker import directory_walker
from purgeraw.deletion import fake_deleter, deleter
from purgeraw.index_extraction import indexer
from purgeraw.purger import purge


@click.command("praw")
@click.option("-i", "--input", "input_path", required=True, type=click.Path(exists=True),
              help="Directory to be purged.")
@click.option("-d", "--delete", "do_delete", is_flag=True,
              help="By default praw will just explain what would be removed. Add this flag to perform the deletion.")
@click.option("-r", "--raw_exts", multiple=True, type=str, default=["cr3", "xmp"], show_default=True,
              help="Used to define which extensions denote a raw file.")
@click.option("-p", "--processed_exts", multiple=True, type=str, default=["jpg"], show_default=True,
              help="Used to define which extensions denote a processed file.")
@click.version_option(__version__, prog_name="praw")
def main(input_path: str, do_delete: bool, raw_exts: Tuple[str], processed_exts: Tuple[str]) -> None:
    pipe(
        input_path,
        directory_walker(list(raw_exts + processed_exts)),
        purge(list(raw_exts), indexer),
        deleter if do_delete else fake_deleter
    )


if __name__ == "__main__":
    main()
