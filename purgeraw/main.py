from typing import Tuple

import click

from purgeraw.directory_service import directory_walker
from purgeraw.indexer_service import indexer
from purgeraw.purge_service import purger
from purgeraw.file_service import fake_delete, delete, raw_determinator


@click.command("Purge Raw")
@click.option("-i", "--input", "input_path", required=True, type=click.Path(exists=True), help="Directory to be purged")
@click.option("-d", "--dryrun", "dry_run", is_flag=True,
              help="Just explain what would be removed, doesn't remove files")
@click.option("-r", "--raw_exts", multiple=True, type=str, default=["cr3"])
@click.option("-p", "--processed_exts", multiple=True, type=str, default=["jpg"])
def main(input_path: str, dry_run: bool, raw_exts: Tuple[str], processed_exts: Tuple[str]) -> None:
    purge = purger(directory_walker(list(raw_exts + processed_exts)),
                   fake_delete if dry_run else delete,
                   raw_determinator(list(raw_exts)),
                   indexer)

    purge(input_path)


if __name__ == "__main__":
    main()
