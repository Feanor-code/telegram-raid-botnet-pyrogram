import asyncio
from dataclasses import dataclass
from io import TextIOWrapper
import json
from typing import Generator, Any
import os

from pyrogram import Client
from rich.console import Console
from rich.prompt import Prompt


console = Console()


@dataclass
class SessionsSettings:
    path: str

    def ask(self) -> (bool | None):
        sessions: list[tuple[str, TextIOWrapper]] = list(self.get_sessions())

        if len(sessions) == 0:
            return console.print(
                "[bold red]You need to add sessions (Telegram accounts)"
            )
    
        try:
            self.raw_sessions = [
                Client(
                    name=session_path,
                    session_string=session_data["session"],
                    api_id=session_data["api_id"],
                    api_hash=session_data["api_hash"],
                    device_model=session_data["device_model"],
                    app_version=session_data["app_version"],
                    system_version=session_data["system_version"]
                )
                for session_path, session_data in sessions
            ]
        except Exception as error:
            return console.print(error, style="bold red")

        if result := Prompt.ask("Initialize sessions?", choices=["y", "n"], default="n") == "y":
            with console.status("Connection..."):
                self.sessions = [
                    session for session in asyncio.get_event_loop().run_until_complete(
                        asyncio.gather(*[
                            self.launch(session)
                            for session in self.raw_sessions
                        ])
                    )
                    if session is not None
                ]
        
        return result

    async def launch(self, session: Client) -> (Client | None):
        try:
            await session.start()
        except Exception as error:
            console.print(
                f"[bold red]Deleted session. Error : {error}"
            )

            os.remove(session.name)
            return
        
        else:
            console.log(session.name)
            return session

    def get_sessions(self) -> Generator[tuple[str, Any], Any, None]:
        for file in os.listdir("sessions"):
            if file.endswith(".session"):
                session_path = os.path.join(self.path, file)
                
                with open(session_path) as file:
                    try:
                        session_data = json.load(file)

                    except Exception as error:
                        console.print(
                            session_path,
                            error,
                            style="bold white"
                        )
                        
                    else:
                        yield session_path, session_data