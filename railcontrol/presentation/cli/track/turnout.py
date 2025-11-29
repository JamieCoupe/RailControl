import typer

from rich.console import Console
from rich.table import Table

from railcontrol.domain.domain_enums import TrackBlockClass, TurnoutState
from railcontrol.application.app_context import AppDataContext
from railcontrol.config import DATA_PATH

turnout_app = typer.Typer(help="Turnout commands")
console = Console()


@turnout_app.command("list")
def list_turnouts():
    context = AppDataContext(DATA_PATH)

    # Create rich table
    table = Table(title="Turnotus")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("ID", style="magenta")
    table.add_column("Type", style="blue")
    table.add_column("Current State", style="blue")
    table.add_column("Start Section", style="green")
    table.add_column("Diverging Section", style="green")


    for turnout in context.repos.turnouts.get_all():
        table.add_row(
            turnout.name,
            turnout.id,
            turnout.turnout_type.value,
            turnout.current_state.value,
            turnout.straight_section_id,
            turnout.diverging_section_id,
        )

    console.print(table)

@turnout_app.command("set")
def set_turnout(turnout_id: str, state: str):
    console.print(f"Would set turnout {turnout_id} to {state}")

@turnout_app.command("toggle")
def set_turnout(turnout_id: str):
    console.print(f"Would toggle turnout {turnout_id}")

@turnout_app.command("add")
def add_turnout(turnout_id: str, name: str):
    console.print(f"Adding turnout {turnout_id} ({name})")