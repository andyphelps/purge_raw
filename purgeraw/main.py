import click

from purgeraw.purge_orchestrator import PurgeOrchestrator


@click.command("Purge Raw")
@click.option("-i", "--input", "input_path", required=True, type=click.Path(exists=True), help="Input Directory")
@click.option("-d", "--dryrun", "dry_run", is_flag=True)
def main(input_path: str, dry_run: bool) -> None:
    purger = PurgeOrchestrator()
    purger.purge(input_path, dry_run)
