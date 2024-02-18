from pathlib import Path

import typer
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager

from amsdal_cli.commands.deploy.app import sub_app
from amsdal_cli.commands.deploy.enums import DeployType
from amsdal_cli.commands.deploy.enums import LakehouseOption
from amsdal_cli.utils.cli_config import CliConfig


@sub_app.callback(invoke_without_command=True)
def deploy_command(
    ctx: typer.Context,
    deploy_type: DeployType = DeployType.INCLUDE_STATE_DB,
    lakehouse_type: LakehouseOption = LakehouseOption.POSTGRES,
) -> None:
    """
    Deploy the app to the Cloud Server.
    """

    if ctx.invoked_subcommand is not None:
        return

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()
    manager.deploy(
        deploy_type=deploy_type.value,
        lakehouse_type=lakehouse_type.value,
        application_uuid=cli_config.application_uuid,
        application_name=cli_config.application_name,
    )
