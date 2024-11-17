import asyncio

from pyrogram import Client
from rich.console import Console

from modules.base.base import BaseFunction
from utils.session_settings import SessionSettings


console = Console()


class FastFlood(SessionSettings, BaseFunction):
    """Fast flood"""

    async def ask(self) -> None:
        self.link = await self.change_link(
            console.input("[bold red]link> ")
        )

    async def fast_flood(self, session: Client, chat_id: int) -> None:
        try:
            await session.send_message(chat_id, "@yi_pedic_i_vse че в хуй скажешь? аллоооооо сын бляди")
        except Exception as error:
            console.print(error)

    async def execute(self, session: Client) -> None:
        try:
            chat = await session.get_chat(self.link)

            await asyncio.gather(*[
                self.fast_flood(session, chat.id)
                for _ in range(100)
            ])
        except Exception as error:
            console.print(error)