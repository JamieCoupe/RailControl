import typer
from rich.console import Console
from rich.table import Table


timetable_app = typer.Typer(help="Timetable-related commands")
console = Console()


@timetable_app.command("generate")
def generate_timetable(file: str, start: str = "08:00"):
    typer.echo(f"Would generate timetable from {file}, starting at {start}")

