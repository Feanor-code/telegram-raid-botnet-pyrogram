import asyncio
import random

from pyrogram import Client
from pyrogram.errors.exceptions import UserAlreadyParticipant
from rich.console import Console
from rich.prompt import Confirm

from modules.flood import Flood


console = Console()


class JoinChat(Flood):
    """Join chat"""

    async def ask(self) -> None:
        print()
        
        console.print(
            "[1] Join the chat",
            "[2] Join the channel chat",
            sep="\n",
            style="bold white"
        )
        self.mode = console.input("[bold white]>> ")

        print()

        self.link = await self.change_link(
            console.input("[bold red]link> ")
        )
        self.delay = await self.delay_ask()
        self.is_flood = Confirm.ask("[bold red]Flood after joining?")
        
        if self.is_flood:
            await super().ask()
    
    async def join_chat(self, session: Client) -> None:
        try:
            if self.mode == "2":
                group = await session.get_chat(self.link)
                return await session.join_chat(group.linked_chat.id)

            await session.join_chat(self.link)
        except UserAlreadyParticipant:
            pass

        except Exception as error:
            return console.print(f"Didn't join the chat. Error : {error}")
        
        finally:
            await asyncio.sleep(random.randint(
                *self.delay
            ))

    async def execute(self, session: Client) -> None:
        await self.join_chat(session)

        if self.is_flood:
            await super().flood(session)