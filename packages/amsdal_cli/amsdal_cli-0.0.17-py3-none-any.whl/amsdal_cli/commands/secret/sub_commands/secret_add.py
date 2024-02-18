from pathlib import Path

import typer
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager

from amsdal_cli.commands.secret.app import sub_app
from amsdal_cli.utils.cli_config import CliConfig


@sub_app.command(name='add')
def secret_add_command(
    ctx: typer.Context,
    secret_name: str,
    secret_value: str,
) -> None:
    """
    Add secrets to your Cloud Server app.
    """

    if ctx.invoked_subcommand is not None:
        return

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()
    manager.add_secret(
        secret_name=secret_name,
        secret_value=secret_value,
        application_uuid=cli_config.application_uuid,
        application_name=cli_config.application_name,
    )
