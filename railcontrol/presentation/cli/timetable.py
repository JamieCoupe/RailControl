import typer
from rich.console import Console
from rich.table import Table

from railcontrol.application.app_context import AppDataContext
from railcontrol.application.routing.passenger_route_expander import PassengerRouteExpander
from railcontrol.application.timetable.running_time_calculator import RunningTimeCalculator
from railcontrol.application.timetable.running_time_engine import RunningTimeEngine
from railcontrol.application.timetable.service_id_generator import ServiceIDGenerator
from railcontrol.application.timetable.timetable_engine import TimetableEngine
from railcontrol.application.timetable.timetable_validator import TimetableValidator
from railcontrol.application.utils.time_format import seconds_to_hhmm
from railcontrol.config import default_route_file
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute
from railcontrol.infrastructure.data_sources.yaml.passenger_route_loader import PassengerRouteYamlLoader
from railcontrol.infrastructure.repository.yaml.yaml_passenger_route_repository import YamlPassengerRouteRepository
from railcontrol.presentation.cli.context import context

timetable_app = typer.Typer(help="Timetable-related commands")
console = Console()



@timetable_app.command("generate")
def generate_timetable(route_id: str, start_time: int, profile: str = "express"):
    """
    Generate a fully timestamped timetable for a passenger route.

    start_time = seconds since midnight
    """

    # context = AppDataContext()

    loader = PassengerRouteYamlLoader(default_route_file)
    route_repo = YamlPassengerRouteRepository(loader)
    route = route_repo.get(route_id)

    expander = PassengerRouteExpander(
        context.repos.stations,
        context.repos.track_blocks,
        context.repos.track_sections,
        context.routing,
    )

    expanded_route: ExpandedPassengerRoute = expander.expand_route(route)

    # Compute running times first
    calculator = RunningTimeCalculator()
    rt_engine = RunningTimeEngine(calculator)
    rt_engine.compute_for_route(expanded_route, profile)

    # Build timetable
    tt_engine = TimetableEngine()
    rows = tt_engine.generate_timetable(expanded_route, start_time_seconds=start_time)
    TimetableValidator.validate(rows)
    service_id_generator = ServiceIDGenerator()
    service_id = service_id_generator.generate_headcode(profile, expanded_route)

    # Render table
    table = Table(title=f"Timetable for service {service_id}")
    table.add_column("Station", style="cyan")
    table.add_column("Arr (s)", style="yellow")
    table.add_column("Dep (s)", style="green")
    table.add_column("Dwell (s)", style="magenta")
    table.add_column("Runtime (s)", style="blue")

    for row in rows:
        table.add_row(
            row.station_id,
            seconds_to_hhmm(row.arrival_s),
            "-" if row.departure_s is None else seconds_to_hhmm(row.departure_s),
            str(row.dwell_s),
            str(row.runtime_s),
        )

    console.print(table)
@timetable_app.command("running-time")
def generate_timetable(route_id: str, profile: str):
    typer.echo(f"Will generate runtime calculation for route {route_id}, with profile {profile}")

    loader = PassengerRouteYamlLoader(default_route_file)
    route = YamlPassengerRouteRepository(loader).get(route_id)

    expander = PassengerRouteExpander(
        context.repos.stations,
        context.repos.track_blocks,
        context.repos.track_sections,
        context.routing,
    )
    expanded_route = expander.expand_route(route)

    calculator = RunningTimeCalculator()
    engine = RunningTimeEngine(calculator)
    engine.compute_for_route(expanded_route, profile)

    table = Table(title="Running Time Breakdown")
    table.add_column("Segment", style="cyan")
    table.add_column("Length (mm)", style="magenta")
    table.add_column("Eff Speed (mph)", style="blue")
    table.add_column("Time (s)", style="green")
    table.add_column("Cumulative (s)", style="green")

    cumulative = 0

    for leg in expanded_route.legs:

        # Station summary row
        table.add_row(
            f"[bold]{context.repos.stations.get(leg.station_id).name}[/bold]",
            str(leg.total_length_mm),
            str(leg.effective_speed_mph),
            str(leg.running_time_s),
            str(cumulative + leg.running_time_s),
        )
        cumulative += leg.running_time_s

        # Now insert each inbound edge underneath
        for edge_calc in leg.edge_calculations:
            table.add_row(
                f"  └─ {edge_calc['block_id']}",
                str(edge_calc["length_mm"]),
                str(edge_calc["effective_speed_mph"]),
                str(edge_calc["time_s"]),
                str(cumulative + edge_calc["time_s"]),
            )
            cumulative += edge_calc["time_s"]

    console.print(table)
