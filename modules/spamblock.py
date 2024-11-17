import asyncio
import re

from pyrogram import Client
from pyrogram.errors import BadRequest

from rich import box
from rich.table import Table
from rich.console import Console


console = Console()


class SpamBlock:
    """Checking the status of accounts"""

    async def ask(self) -> None:
        self.table = Table(box=box.ROUNDED)
        
        for name in [
            "Name", 
            "Number", 
            "Block"
        ]:
            self.table.add_column(name)

    async def execute(self, session: Client) -> None:
        try:
            await session.send_message(
                "SpamBot",
                "/start"
            )
        except BadRequest:
            await session.unblock_user(178220800)
            await self.execute(session)

        await asyncio.sleep(1)
        me = await session.get_me()

        messages = session.get_chat_history("SpamBot", limit=1)
        message = [text async for text in messages][0]

        if message.text == "/start":
            await self.checking_block(session)

        else:
            string = message.text.split("\n")

            if len(string) != 1:
                date = re.findall(r"\d+\s\w+\s\d{4}", message.text)

                if date:
                    result = date[0]

                else:
                    result = "[bold red][-][/]"

            else:
                result = "[bold green][+][/]"

        self.table.add_row(
            me.first_name,
            me.phone_number,
            result
        )

    def prt(self) -> None:
        console.print(self.table)
