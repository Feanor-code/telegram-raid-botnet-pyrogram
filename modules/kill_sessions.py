from typing import Literal

from pyrogram import Client
from pyrogram.raw import functions, types
from pyrogram.errors import HashInvalid

from rich.console import Console


console = Console()


class ResetAuth:
    """End all other sessions"""

    async def ask(self) -> (Literal[True] | None):
        if console.input("[bold red]Are you sure? (y/n): ") != "y":
            return True

    async def execute(self, session: Client) -> None:
        account: types.account.authorizations = await session.invoke(
            functions.account.GetAuthorizations()
        )

        for authorization in account.authorizations:
            try:
                await session.invoke(functions.account.ResetAuthorization(hash=authorization.hash))
                console.print(
                    "[bold]Session deactivated: ({device}, {app_name}, {app_version}) -> [bold red]{account_hash}[/]"
                    .format(
                        device=authorization.device_model, 
                        app_name=authorization.app_name,
                        app_version=authorization.app_version, 
                        account_hash=authorization.hash
                    )
                )
            except HashInvalid:
                continue
            except Exception as error:
                console.print(f"Session not completed. Error : {error}")