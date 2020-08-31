import click

from purgeraw.purge_orchestrator import PurgeOrchestrator


@click.command("Purge Raw")
@click.option("-i", "--input", "input_path", required=True, type=click.Path(exists=True), help="Directory to be purged")
@click.option("-d", "--dryrun", "dry_run", is_flag=True,
              help="Just explain what would be removed, doesn't remove files")
def main(input_path: str, dry_run: bool) -> None:
    purger = PurgeOrchestrator()
    purger.purge(input_path, dry_run)


if __name__ == "__main__":
    main()
