import typer
import os

from rich.console import Console

from railcontrol.presentation.cli.track.turnout import turnout_app
from railcontrol.presentation.cli.track.block import track_block_app
from railcontrol.presentation.cli.track.section import track_section_app
from railcontrol.presentation.cli.station import stations_app
from railcontrol.presentation.cli.industry import industry_app
from railcontrol.presentation.cli.route import route_app
from railcontrol.presentation.cli.timetable import timetable_app


app = typer.Typer(help="RailControl - CLI tools for railway operations")


app.add_typer(route_app, name="route")
app.add_typer(timetable_app, name="timetable")
app.add_typer(stations_app, name="station")
app.add_typer(industry_app, name="industry")

#Track parent app
track_app = typer.Typer(help="Track-related commands")
app.add_typer(track_app, name="track")

# Nested sub-apps
track_app.add_typer(track_block_app, name="block")
track_app.add_typer(track_section_app, name="section")
track_app.add_typer(turnout_app, name="turnout")


console = Console()


def main():
    app()

if __name__ == "__main__":
    main()