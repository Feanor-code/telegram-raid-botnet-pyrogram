import asyncio

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
    async def execute(self, session: str, data: tuple) -> None:
        print(data)
        await asyncio.sleep(1)