import json
from pathlib import Path

import typer
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table

from amsdal_cli.commands.deploy.enums import OutputFormat
from amsdal_cli.commands.secret.app import sub_app
from amsdal_cli.utils.cli_config import CliConfig


@sub_app.command(name='list')
def secret_list_command(
    ctx: typer.Context,
    output: OutputFormat = OutputFormat.DEFAULT,
    *,
    values: bool = False,
) -> None:
    """
    List the app secrets on the Cloud Server.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()
    list_response = manager.list_secrets(
        with_values=values,
        application_uuid=cli_config.application_uuid,
        application_name=cli_config.application_name,
    )

    if not list_response:
        return

    if output == OutputFormat.JSON:
        print(json.dumps(list_response.model_dump(), indent=4))
        return

    if not list_response.secrets:
        print('No secrets found.')
        return

    data_table = Table()
    data_table.add_column('Secret Name', justify='center')

    if values:
        data_table.add_column('Secret Value', justify='center')

    for secret in list_response.secrets:
        if values:
            secret_name, secret_value = secret.split('=', 1)
            data_table.add_row(secret_name, secret_value)
        else:
            data_table.add_row(secret)

    print(data_table)
