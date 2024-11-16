from typing import Literal

from pyrogram import Client
from rich.console import Console


console = Console()


class LeaveChat:
    """Leave the chat"""

    async def ask(self) -> (Literal[True] | None):
        if console.input("[bold red]Are you sure? (y/n): ") != "y":
            return True
        
    async def execute(self, session: Client) -> None:
        try:
            me = await session.get_me()
            async for dialog in session.get_dialogs():
                await session.leave_chat(dialog.chat.id, delete=True)
                console.log(
                    "[*] User {name} has left the [yellow]{chat}[/] chat"
                    .format(name=me.first_name, chat=dialog.chat.first_name if dialog.chat.first_name else dialog.chat.title)
                )

        except Exception as error:
            console.print("Error : {}".format(error), style="bold white")