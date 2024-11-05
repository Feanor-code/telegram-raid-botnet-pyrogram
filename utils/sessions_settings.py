from dataclasses import dataclass

from rich.prompt import Prompt



@dataclass
class SessionsSettings:
    path: str

    def ask(self) -> None:
        self.initialize = Prompt.ask("Initialize sessions?", choices=["y", "n"], default="n")

    async def parse_sessions(self) -> None:
        ...

    async def initialization(self) -> None:
        ...