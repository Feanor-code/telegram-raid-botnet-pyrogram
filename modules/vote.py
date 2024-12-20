from pyrogram import Client
from pyrogram.types import Poll
from rich.console import Console

from modules.base.base import BaseFunction


console = Console()


class Vote(BaseFunction):
    """Vote in poll"""

    async def ask(self) -> None:
        self.option = int(console.input("[bold red]Write the option number: "))-1
        self.group_id, self.message_id = await self.parse_message_id()

    async def vote(self, session: Client) -> Poll:
        return await session.vote_poll(
            self.group_id,
            self.message_id,
            self.option
        )

    async def execute(self, session: Client) -> None:
        try:
            me = await session.get_me()
            poll_data = await self.vote(session)

            console.print(
                "[*] Option {option} selected ({name})"
                .format(
                    option=poll_data.options[self.option].text,
                    name=me.first_name
                )
            )
        except Exception as error:
            return console.print(f"Account cannot vote. Error : {error}")