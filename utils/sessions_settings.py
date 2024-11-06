import asyncio
from dataclasses import dataclass

from rich.console import Console
from rich.prompt import Prompt

from utils.get_sessions import get_sessions


console = Console()


@dataclass
class SessionsSettings:
    path: str

    def ask(self) -> (bool | None):
        sessions = get_sessions()

        if len(sessions) == 0:
            return console.log("No sessions")

        if result := Prompt.ask("Initialize sessions?", choices=["y", "n"], default="n") == "y":
            asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*[
                    self.launch(session)
                    for session in sessions
                ])
            )
        
        return result

    async def parse_sessions(self) -> None:
        ...

    async def launch(self, session: str) -> None:
        ...