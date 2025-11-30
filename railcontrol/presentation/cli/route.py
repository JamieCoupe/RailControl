import typer
import os

from rich.console import Console
from rich.table import Table

from railcontrol.application.app_context import AppDataContext
from railcontrol.application.routing.passenger_route_expander import PassengerRouteExpander
from railcontrol.application.timetable.block_occupancy_generator import BlockOccupancyGenerator
from railcontrol.domain.track.track_block import PlatformTrackBlock
from railcontrol.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader
from railcontrol.infrastructure.repository.yaml.yaml_passenger_route_repository import YamlPassengerRouteRepository
from railcontrol.config import DATA_PATH, default_route_file

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


@route_app.command("occupancy", help="Generate block occupancy timeline")
def generate_occupancy(route_id: str, start_time:int, service_id: str, route_file: str = "test"):

    if not os.path.exists(route_file):
        typer.echo(f'Route file at {route_file} doesnt exist')
        typer.echo(f'defaulting to {default_route_file}')
        route_file = default_route_file

    context = AppDataContext(DATA_PATH)
    loader = PassengerRouteYamlLoader(route_file)
    route = YamlPassengerRouteRepository(loader).get(route_id)

    expander = PassengerRouteExpander(
        context.repos.stations,
        context.repos.track_blocks,
        context.repos.track_sections, context.routing)
    expanded_route = expander.expand_route(route)

    generator = BlockOccupancyGenerator(
        service_id=service_id,
        start_time=start_time,
        expanded_route=expanded_route
    )

    block_occupancy = generator.generate()

    # Create rich table
    table = Table(title=f"Block Occupancy for - {service_id }")
    table.add_column("Block ID", style="cyan", no_wrap=True)
    table.add_column("Junction > Junction", style="green")
    table.add_column("Entry Time", style="yellow")
    table.add_column("Exit Time", style="yellow")
    table.add_column("Section Length (mm)", style="magenta")
    table.add_column("Max Speed", style="green")

    for block in block_occupancy:
        table.add_row(
            block.block_id,
            f"{block.source_start_junction} → {block.source_end_junction}",
            str(block.t_entry),
            str(block.t_exit),
            str(block.length_mm),
            str(block.max_speed),

        )

    console.print(table)