import sys
import typer
from .core import execute_install, execute_publish, execute_server, run_plugin_yaml, clear_pkg_cache

app = typer.Typer(add_completion=False)


def main():
    app()


@app.command()
def install():
    execute_install()


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def publish():
    execute_publish(' '.join(['npm', 'publish', *sys.argv[2:]]))


@app.command()
def server():
    execute_server(False)


@app.command()
def serverfull():
    execute_server(True)


@app.command()
def clearcache():
    clear_pkg_cache()


@app.command()
def yaml():
    run_plugin_yaml()
