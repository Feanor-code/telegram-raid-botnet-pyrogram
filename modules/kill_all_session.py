from typing import Literal

from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.errors import HashInvalid

from rich.console import Console


console = Console()


class ResetAuth:
    """End all other sessions"""

    async def ask(self) -> (Literal[True] | None):
        if console.input("[bold red]Are you sure? (y/n): ") != "y":
            return True

    async def execute(self, session: Client) -> None:
        account = await session.invoke(functions.account.GetAuthorizations())

        for x in account.authorizations[::1]:
            try:
                await session.invoke(functions.account.ResetAuthorization(hash=x.hash))

            except HashInvalid:
                continue

            except Exception as error:
                console.print("Session not completed. Error : {}".format(error), style="bold white")

            else:
                console.print(
                    "[bold]Kill: ({device}, {ip}) -> [bold red]{account_hash}[/]"
                    .format(device=x.device_model, ip=x.ip, account_hash=x.hash)
                )