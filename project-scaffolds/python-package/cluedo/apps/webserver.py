import click
from cluedo.www import create_app

@click.command()
@click.option("--port")
def run(port):
    app = create_app()
    app.run()

if __name__ == "__main__":
    run()