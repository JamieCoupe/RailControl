import typer
import os
from rich.console import Console
from rich.table import Table

from railcontrol.application.app_context import AppDataContext
from railcontrol.config import DATA_PATH

track_section_app = typer.Typer(help="Track section commands")
console = Console()



@track_section_app.command("list")
def list_sections():
    context = AppDataContext(DATA_PATH)

    # Create rich table
    table = Table(title="Track Sections")
    table.add_column("ID", style="magenta")
    table.add_column("Block ID", style="magenta")
    table.add_column("Start Junction", style="blue")
    table.add_column("End Junction", style="blue")
    table.add_column("Length (mm)", style="green")
    table.add_column("Max Speed (MPH)", style="green")

    for section in context.repos.track_sections.get_all():
        table.add_row(
            section.id,
            section.block_id,
            section.start_junction_id,
            section.end_junction_id,
            str(section.length_mm),
            str(section.max_speed)
        )

    console.print(table)

@track_section_app.command("add")
def add_section(section_id: str):
    console.print(f"Adding section {section_id}")