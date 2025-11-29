import typer


from rich.console import Console
from rich.table import Table

from railcontrol.domain.domain_enums import TrackBlockClass
from railcontrol.application.app_context import AppDataContext
from railcontrol.config import DATA_PATH

track_block_app = typer.Typer(help="Track block commands")
console = Console()

@track_block_app.command("list")
def list_blocks():
    context = AppDataContext(DATA_PATH)

    # Create rich table
    table_all = Table(title="Track Blocks - Standard")
    table_all.add_column("Name", style="cyan", no_wrap=True)
    table_all.add_column("ID", style="magenta")
    table_all.add_column("Class", style="blue")
    table_all.add_column("Type", style="blue")

    # Create rich table
    table_platform = Table(title="Track Blocks - Platform")
    table_platform.add_column("Name", style="cyan", no_wrap=True)
    table_platform.add_column("ID", style="magenta")
    table_platform.add_column("Class", style="blue")
    table_platform.add_column("Type", style="blue")
    table_platform.add_column("Station name", style="green")
    table_platform.add_column("Platform Number", style="green")
    table_platform.add_column("Dwell Time", style="green")

    # Create rich table
    table_industry = Table(title="Track Blocks - Industry")
    table_industry.add_column("Name", style="cyan", no_wrap=True)
    table_industry.add_column("ID", style="magenta")
    table_industry.add_column("Class", style="blue")
    table_industry.add_column("Type", style="blue")
    table_industry.add_column("Industry Name", style="green")
    table_industry.add_column("Loading Time", style="green")


    for block in context.repos.track_blocks.get_all():
        if block.track_block_class == TrackBlockClass.MAINLINE:
            table_all.add_row(
                block.name,
                block.id,
                block.track_block_class.value,
                block.track_block_type.value
            )

        elif block.track_block_class == TrackBlockClass.PLATFORM:

            station_name = context.repos.stations.get(block.station_id).name
            table_platform.add_row(
                block.name,
                block.id,
                block.track_block_class.value,
                block.track_block_type.value,
                station_name,
                str(block.platform_number),
                str(block.dwell_time_minutes)
            )
        else:
            industry_name = context.repos.industries.get(block.industry_id).name
            table_industry.add_row(
                block.name,
                block.id,
                block.track_block_class.value,
                block.track_block_type.value,
                industry_name,
                str(block.load_time_minutes)
            )

    console.print(table_all)
    console.print(table_platform)
    console.print(table_industry)

@track_block_app.command("add")
def add_block(block_id: str, name: str):
    console.print(f"Adding block {block_id} ({name})")