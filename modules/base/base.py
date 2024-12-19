import asyncio
import random

from rich.console import Console
from rich.prompt import Prompt


console = Console()


class BaseFunction:
    async def change_link(self, link: str) -> (int | str):
        if link.isdigit():
            return int(link)
        
        if "/+" in link:
            return link
        
        return link.split("/")[-1]
    
    async def parse_message_id(self):
        link = console.input("[bold red]link to messages> ").split("/")
        group_id = link[-2]
        post_id = int(link[-1])

        if group_id.isdigit():
            group_id = int(f"-100{group_id}")

        return group_id, post_id
    
    async def delay(self, ask: bool | None = None) -> None:
        if ask is not None:
            self.raw_delay = Prompt.ask("[bold red]delay[/]", default="1-2")
            return

        if "-" not in self.raw_delay:
            return await asyncio.sleep(int(self.raw_delay))
        
        return await asyncio.sleep(
            random.randint(
                *tuple(map(int, self.raw_delay.split("-")))
            )
        )