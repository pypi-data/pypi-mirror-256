from amsdal_cli.app import app
from amsdal_cli.commands.secret.app import sub_app
from amsdal_cli.commands.secret.sub_commands import *  # noqa

app.add_typer(sub_app, name='secret')
