import asyncio
import os
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

    async def ask(self, inside: bool | None = None) -> None:
        print()

        for index, function in enumerate(self.choices, 1):
            console.print(
                "[bold white][{index}] {name}"
                .format(index=index, name=function[0])
            )
        self.mode = self.choices[int(console.input("[bold]> "))-1][1]

        print()

        if inside is None:
            self.link = await self.change_link(
                console.input("[bold red]link(or ID)> ")
            )
        await self.delay(ask=True)

    async def flood_text(self, session: Client, chat_id: int) -> None:
        await session.send_message(chat_id, random.choice(self.messages))

    async def flood_photo(self, session: Client, chat_id: int) -> None:
        file = random.choice(os.listdir(os.path.join("resources", "photo")))

        await session.send_photo(
            chat_id,
            os.path.join(
                "resources", "photo", 
                file
            )
        )

    async def flood(
        self, 
        session: Client,
        me: dict,
        chat_id: int
    ) -> None:
        successes = 0
        errors = 0

        while successes < self.message_count:
            try:
                await self.mode(session, chat_id)
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
                    return await session.leave_chat(chat_id, delete=True)
                
                await self.delay()

    async def execute(self, session: Client) -> None:
        me = await session.get_me()
        chat = await session.get_chat(self.link)

        await self.flood(session, me, chat.id)