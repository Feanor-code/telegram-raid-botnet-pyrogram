import asyncio
import random

from rich.prompt import Prompt


class BaseFunction:
    async def change_link(self, link: str) -> str:
        if link.isdigit():
            return int(link)
        
        if "/+" in link:
            return link
        
        return link.split("/")[-1]
    
    async def delay(self, ask: bool | None = None) -> tuple:
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