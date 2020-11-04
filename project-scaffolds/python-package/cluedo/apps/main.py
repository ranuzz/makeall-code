import click

@click.command()
@click.option("--option")
def run(option):
    # noop
    print("Running app with options : {0}".format(option))
