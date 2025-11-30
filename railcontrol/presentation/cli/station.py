import typer
import os
from rich.console import Console
from rich.table import Table

from railcontrol.presentation.cli.context import context

stations_app = typer.Typer(help="Station-related commands")
console = Console()

@stations_app.command("list")
def list_stations():

    # Create rich table
    table = Table(title="Stations")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("ID", style="magenta")
    table.add_column("Number of Platforms", style="green")

    for station in context.repos.stations.get_all():
        table.add_row(station.name, station.id, str(len(station.track_blocks)))


    console.print(table)
