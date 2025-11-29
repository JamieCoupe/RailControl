import typer
import os

from rich.console import Console
from rich.table import Table

from src.application.app_context import AppDataContext
from src.application.routing.passenger_route_expander import PassengerRouteExpander
from src.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader
from src.infrastructure.repository.yaml.yaml_passenger_route_repository import YamlPassengerRouteRepository

app = typer.Typer(help="RailControl - CLI tools for railway operations")

route_app = typer.Typer(help="Route-related commands")
timetable_app = typer.Typer(help="Timetable-related commands")
stations_app = typer.Typer(help="Station-related commands")

app.add_typer(route_app, name="route")
app.add_typer(timetable_app, name="timetable")
app.add_typer(stations_app, name="stations")

console = Console()

# Create context data path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_PATH = os.path.join(ROOT, "data")

@route_app.command("list_id")
def list_route(file:str):
    if not os.path.exists(file):
        raise FileExistsError(f'Route file at {file} doesnt exist')
    passenger_routes = PassengerRouteYamlLoader(file).load()
    for route in passenger_routes['passenger_routes']:
        print(f"Route id: {route['id']}")

@route_app.command("expand")
def expand_route(file: str, route_id: str):
    if not os.path.exists(file):
        raise FileExistsError(f'Route file at {file} doesnt exist')
    context = AppDataContext(DATA_PATH)
    loader = PassengerRouteYamlLoader(file)
    route = YamlPassengerRouteRepository(loader).get(route_id)

    expander = PassengerRouteExpander(
        context.repos.stations,
        context.repos.track_blocks,
        context.repos.track_sections, context.routing)
    expanded = expander.expand_route(route)

    # Create rich table
    table = Table(title="Expanded Passenger Route")
    table.add_column("Station", style="cyan", no_wrap=True)
    table.add_column("Platform", style="magenta")
    table.add_column("Inbound Edges", style="green")

    for leg in expanded.legs:
        table.add_row(
            leg.station_id,
            leg.platform_block_id,
            str(len(leg.inbound_path_edges))
        )
    console.print(table)


@timetable_app.command("generate")
def generate_timetable(file: str, start: str = "08:00"):
    typer.echo(f"Would generate timetable from {file}, starting at {start}")

@stations_app.command("list")
def list_stations():
    typer.echo("Would list stations")

def main():
    app()

if __name__ == "__main__":
    main()