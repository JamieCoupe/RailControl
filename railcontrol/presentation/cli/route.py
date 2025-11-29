import typer
import os

from rich.console import Console
from rich.table import Table

from railcontrol.application.app_context import AppDataContext
from railcontrol.application.routing.passenger_route_expander import PassengerRouteExpander
from railcontrol.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader
from railcontrol.infrastructure.repository.yaml.yaml_passenger_route_repository import YamlPassengerRouteRepository
from railcontrol.config import DATA_PATH

route_app = typer.Typer(help="Route-related commands")
console = Console()

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