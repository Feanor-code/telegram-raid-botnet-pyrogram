import asyncio
import random

from pyrogram import Client
from rich.console import Console

from modules.base.base import BaseFunction
from utils.storage_settings import Settings

console = Console()


class FastFlood(Settings, BaseFunction):
    """Fast flood"""

    def __init__(self) -> None:
        super().__init__()
        console.print(
            "[bold red]Run this function Async. I do not recommend using less than 15 accounts."
        )

    async def ask(self) -> None:
        self.link = await self.change_link(
            console.input("[bold red]link> ")
        )

    async def fast_flood(self, session: Client, chat_id: int) -> None:
        try:
            await session.send_message(chat_id, random.choice(self.messages))
        except Exception:
            pass

    async def execute(self, session: Client) -> None:
        try:
            chat = await session.get_chat(self.link)

            await asyncio.gather(*[
                self.fast_flood(session, chat.id)
                for _ in range(self.message_count)
            ])
        except Exception as error:
            return console.print(
                f"Messages will not be sent. Error : {error}"
            )