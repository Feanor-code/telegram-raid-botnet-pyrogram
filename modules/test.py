import asyncio

from pyrogram import Client
from rich.console import Console


console = Console()


class Flood:
    """Test епта"""

    #вопросы пользователю
    async def ask(self) -> None:
        text = console.input(": ")
        name = console.input("> ")

        return (text, name)

    #действие
    async def execute(self, session: Client, data: tuple) -> None:
        print(await session.get_me())
        await asyncio.sleep(1)