import sys

from pyrogram import Client
from pyrogram.raw import types, functions
from pyrogram.errors import HashInvalid

import asyncio
from rich.console import Console


console = Console()


class ResetAuth:
    """Killed all account sessions"""

    async def ask(self) -> None:
        if console.input("[bold red]You sure? (y/n): ") != "y":
            return True

    async def execute(self, session: Client) -> None:
        me = await session.get_me()
        account = await session.invoke(functions.account.GetAuthorizations())

        for x in account.authorizations[::1]:
            try:
                await session.invoke(functions.account.ResetAuthorization(hash=x.hash))

            except HashInvalid:
                continue

            except Exception as error:
                console.print("Error : {}".format(error), style="bold red")

            else:
                console.print(
                    "[bold]Kill: ({device}, {ip}) -> [bold red]{account_hash}[/]"
                    .format(device=x.device_model, ip=x.ip, account_hash=x.hash)
                )