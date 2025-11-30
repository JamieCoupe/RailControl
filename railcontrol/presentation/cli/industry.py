import typer

from rich.console import Console
from rich.table import Table

from railcontrol.application.app_context import AppDataContext
from railcontrol.config import DATA_PATH

industry_app = typer.Typer(help="Industry-related commands")
console = Console()


@industry_app.command("list")
def list_industries():
    context = AppDataContext(DATA_PATH)

    # Create rich table
    table = Table(title="Industries")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("ID", style="magenta")
    table.add_column("Type", style="green")

    for industry in context.repos.industries.get_all():
        table.add_row(
            industry.name,
            industry.id,
            industry.industry_type.value
        )

    console.print(table)

@industry_app.command("list_detail")
def list_industry_detail(industry_id: str):
    context = AppDataContext(DATA_PATH)
    industry = context.repos.industries.get(industry_id)

    # Create HL rich table
    table_industry = Table(title="Industry")
    table_industry.add_column("Name", style="cyan", no_wrap=True)
    table_industry.add_column("ID", style="magenta")
    table_industry.add_column("Type", style="blue")
    table_industry.add_column("Number of lines", style="green")

    lines = context.repos.track_blocks.get_by_industry(industry.id)
    table_industry.add_row(
        industry.name,
        industry.id,
        str(industry.industry_type),
        str(len(lines))
    )

    #Inputs
    table_input = Table(title="Industry - Inputs")
    table_input.add_column("Industry", style="cyan", no_wrap=True)
    table_input.add_column("Input", style="magenta")
    table_input.add_column("Amount", style="green")

    for input in context.repos.industries.get_inputs(industry.id):
        commodity = context.repos.commodities.get(input.commodity_id)
        table_input.add_row(
            industry.name,
            commodity.name,
            str(input.amount)
        )

    #Outputs
    table_output = Table(title="Industry - Outputs")
    table_output.add_column("Industry", style="cyan", no_wrap=True)
    table_output.add_column("Output", style="magenta")
    table_output.add_column("Amount", style="green")


    for output in context.repos.industries.get_outputs(industry.id):
        commodity = context.repos.commodities.get(output.commodity_id)
        table_output.add_row(
            industry.name,
            commodity.name,
            str(output.amount)
        )

    console.print(table_industry)
    console.print(table_input)
    console.print(table_output)

