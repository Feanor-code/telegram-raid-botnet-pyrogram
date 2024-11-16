from rich.prompt import Prompt


class BaseFunction:
    async def change_link(self, link: str) -> str:
        if link.isdigit():
            return int(link)
        
        if "/+" in link:
            return link
        
        return link.split("/")[-1]
    
    async def delay_ask(self) -> tuple:
        delay = Prompt.ask("[bold red]delay[/]", default="1-2")
        return tuple(map(int, delay.split("-")))