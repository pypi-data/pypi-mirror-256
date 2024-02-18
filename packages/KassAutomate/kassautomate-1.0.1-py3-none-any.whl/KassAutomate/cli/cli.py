from rich.console import Console
from rich.table import Table
from typer import Typer
from rich import inspect
from KassOrm import Migration
from KassStorager import Storager

console = Console()
app = Typer()


@app.command()
def hello(name: str):
    """doctest"""

    inspect(name, methods=True)
    console.print(f"Hello {name}", style="bold red")


@app.command()
def start_app(appname: str):
    migrations_dir = Storager(appname).getDir("database/migrations")
    Migration().execute_all_migrations("")


@app.command()
def make_controller(controller_name: str):
    pass


@app.command()
def make_model(model_name: str):
    pass


@app.command()
def make_migration(migration_name: str):
    pass
