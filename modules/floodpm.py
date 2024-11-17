import asyncio
import random

from pyrogram import Client
from rich.console import Console

from modules.base.base import BaseFunction


console = Console()


class FloodMP(BaseFunction):
    """Flood to PM"""

    async def ask(self) -> None:
        self.users = console.input("[bold red]USER: [/]")
        self.text_flood = console.input("[bold red]text> [/]")
        self.delay = await self.delay_ask()        
        

    async def execute(self, session: Client) -> None:
        me = await session.get_me()
        count = 0

        while True:
            try:
                await session.send_message(self.users, self.text_flood)

                count += 1
                console.print(
                    "({name}) [bold green]sent[/] COUNT: {count}"
                    .format(name=me.first_name, count=count)
                )
            except Exception as error:
                console.print("Not sent. Error : %s" % error, style="bold white")

            finally:
                await asyncio.sleep(random.randint(
                    *self.delay
                ))