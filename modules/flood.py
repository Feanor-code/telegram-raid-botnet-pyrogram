import asyncio
import random
from typing import Awaitable

from pyrogram import Client
from pyrogram.errors.exceptions import FloodWait, SlowmodeWait
from rich.console import Console

from modules.base.base import BaseFunction
from utils.storage_settings import Settings


console = Console()


class Flood(BaseFunction, Settings):
    """Flood chat"""

    def __init__(self) -> None:
        super().__init__()
        self.choices = (
            ("Raid text", self.flood_text),
            ("Raid photo", self.flood_photo)
        )

    async def ask(self) -> tuple:
        for index, function in enumerate(self.choices, 1):
            console.print(
                "[bold white][{index}] {name}"
                .format(index=index, name=function[0])
            )
        self.mode = self.choices[int(console.input("[bold]> "))-1][1]

        self.link = await self.change_link(
            console.input("[bold red]link> ")
        )
        self.delay = await self.delay_ask()

    async def flood_text(self, session: Client, chat_id: int) -> None:
        await session.send_message(chat_id, random.choice(self.messages))

    async def flood_photo(self) -> None:
        ...

    async def flood(
        self, 
        session: Client
    ) -> None:
        successes = 0
        errors = 0

        me = await session.get_me()
        chat = await session.get_chat(self.link)

        while successes < self.message_count:
            try:
                await self.mode(session, chat.id)
            except (FloodWait, SlowmodeWait) as wait:
                wait = wait.value

                console.print(f"[bold red]Wait {wait} seconds!")
                await asyncio.sleep(wait)

            except Exception as error:
                errors += 1
                console.print(f"[bold red]Message not Sent. Error : {error}")
            
            else:
                successes += 1
                console.print(
                    "({name}) [bold green]sent[/] COUNT: [magenta]{count}"
                    .format(name=me.first_name, count=successes)
                )

            finally:
                if errors >= 3:
                    return await session.leave_chat(chat.id, delete=True)
                
                await asyncio.sleep(random.randint(
                    *self.delay
                ))

    async def execute(self, session: Client) -> None:
        await self.flood(session)