# RailControl CLI
A modular, DDD-aligned command-line interface for railway operations.

The RailControl CLI provides command-line access to the railway operations domain, including:

- Stations
- Track blocks
- Turnouts
- Industries
- Passenger routes
- Timetable utilities
- Topology inspection
- Freight (future)

It is implemented using Typer, structured as multiple sub-apps, and interacts with the domain via the Application Layer (AppDataContext and, later, query/command services).

------------------------------------------------------------
## Features

- Modular Typer-based CLI
- Separate subcommands per domain area (industry, track, turnout, etc.)
- Uses Rich for formatted tabular output
- Follows Clean Architecture / DDD layering:
  - Presentation (CLI)
  - Application (services, AppDataContext)
  - Domain (entities, value objects, enums)
  - Infrastructure (YAML repositories, loaders)
- Supports nested subcommands (e.g. "track block list")
- YAML-backed repositories configured by DATA_PATH
- Easy to extend with new commands

------------------------------------------------------------
## CLI Structure

The CLI lives under:

    railcontrol/presentation/cli/

Each logical area of the domain has its own CLI module:

    railcontrol/presentation/cli/
    ├── main.py              # Root Typer app; registers all sub-apps
    │
    ├── industry.py          # industry_app
    ├── turnout.py           # turnout_app
    ├── route.py             # route_app
    ├── stations.py          # stations_app
    ├── timetable.py         # timetable_app
    │
    └── track/
        ├── block.py         # track_block_app
        └── section.py       # track_section_app

The CLI entry point is configured in pyproject.toml:

    [project.scripts]
    railcontrol = "railcontrol.presentation.cli.main:app"

Once installed, the "railcontrol" command is available globally in the environment.

------------------------------------------------------------
## Usage

### Top-level help

    railcontrol --help

### Track blocks

    railcontrol track block list
    railcontrol track block add BLOCK01 "Up Main"

### Industries

    railcontrol industry list
    railcontrol industry list_detail IND01

### Turnouts

    railcontrol turnout list
    railcontrol turnout set T01 straight
    railcontrol turnout toggle T01

Each subcommand also exposes its own help:

    railcontrol track --help
    railcontrol track block --help
    railcontrol industry --help
    railcontrol turnout --help

------------------------------------------------------------
## Architecture Overview

The CLI is the Presentation layer in a Clean Architecture / DDD-style design:

    CLI (Typer)
        ↓
    Application Layer (AppDataContext, query/command services)
        ↓
    Domain entities and value objects
        ↓
    Repositories and data sources (YAML, database, etc.)

The CLI:

- Does not implement business rules.
- Does not persist data directly.
- Should not (long term) call repositories directly.
- Is responsible only for:
  - Parsing command line arguments and options.
  - Calling application services / AppDataContext.
  - Presenting results to the user (via Rich tables).

Over time, orchestration logic (multiple repo lookups, joins, decisions) should move into dedicated application services, and the CLI should call those services instead of injecting domain infrastructure directly.

------------------------------------------------------------
## Table Style Guide (Rich)

To keep output consistent across different commands, use a standard set of styles for each type of column. Fill in the styles you want to use (Rich style strings: colour names, bold, italic, etc.).

Suggested style matrix:

    Type of data                Style to use (fill in)
    ---------------------------------------------------------
    IDs                         magenta 
    Names                       cyan 
    Domain types / enums        blue
    Timing / duration           yello
    Station / industry names    green
    Status / state fields       yellow
    Warnings / errors           red  

Example (you will adapt colours to your chosen scheme):

    table.add_column("ID", style="<FILL_ME>")
    table.add_column("Name", style="<FILL_ME>")
    table.add_column("Type", style="<FILL_ME>")
    table.add_column("Dwell Time", style="<FILL_ME>")

You can also standardise table titles, e.g.:

    Table title convention: "[bold <PRIMARY_COLOUR>]...[/]"

Fill this in consistently per domain, for example:
- Track-related tables: "[bold <TRACK_COLOUR>]Track Blocks[/]"
- Industry-related tables: "[bold <INDUSTRY_COLOUR>]Industries[/]"

------------------------------------------------------------
## Development Workflow

### Install the CLI in editable mode

From the project root:

    pip install -e .

This installs the "railcontrol" CLI entry point while keeping the code editable in-place.

### Run the CLI

    railcontrol --help
    railcontrol track block list
    railcontrol industry list

Changes made to the Python files under "railcontrol/presentation/cli/" are picked up immediately in editable mode.

### Run tests

From the project root:

    pytest

------------------------------------------------------------
## Configuration (DATA_PATH)

The CLI uses YAML-backed repositories via AppDataContext. The path to the YAML data directory is centralised (for example in "railcontrol/config.py"):

    from railcontrol.config import DATA_PATH
    context = AppDataContext(DATA_PATH)

This avoids hardcoding filesystem paths in individual CLI modules and keeps configuration at the application / infrastructure boundary.

------------------------------------------------------------
## Adding a New CLI Component

1. Create a new module under "railcontrol/presentation/cli/" (or inside an appropriate subpackage, e.g. "track/"):

       railcontrol/presentation/cli/my_feature.py

2. Inside that module, define a Typer app, for example:

       import typer
       my_feature_app = typer.Typer(help="My new feature commands")

3. Add one or more commands:

       @my_feature_app.command("do_thing")
       def do_thing(...):
           # Call application services here
           ...

4. In "main.py", import and register the new sub-app:

       from .my_feature import my_feature_app
       app.add_typer(my_feature_app, name="myfeature")

5. (Optional) Update this README with new usage examples and any additional table style rules.

------------------------------------------------------------
## Future Improvements (Notes / TODOs)

- Move more of the orchestration logic (multiple repository lookups, joins, calculations) into explicit application services.
- Improve error handling and validation with Rich formatting.
- Add global CLI options (--data-dir, --verbose, --format=json, etc.).
- Add shell completion setup instructions for bash, zsh, PowerShell.
- Introduce DTOs for query results to avoid coupling CLI tables directly to domain entities.
