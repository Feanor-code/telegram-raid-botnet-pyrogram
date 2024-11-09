import asyncio
from dataclasses import dataclass
from io import TextIOWrapper
import json
from typing import Generator, Any
import os

from pyrogram import Client
from rich.console import Console
from rich.prompt import Prompt

from utils.get_sessions import get_sessions


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

        if result := Prompt.ask("Initialize sessions?", choices=["y", "n"], default="n") == "y":
            with console.status("Connection..."):
                sessions = asyncio.get_event_loop().run_until_complete(
                    asyncio.gather(*[
                        self.launch(session)
                        for session in self.raw_sessions
                    ])
                )
                self.sessions = [session for session in sessions if session is not None]
        
        return result

    async def parse_sessions(self) -> None:
        ...

    async def launch(self, session: Client) -> None:
        console.log(session.name)

        try:
            return await session.start()
        
        except Exception as error:
            console.print("Error : {}".format(error))

    def get_sessions(self) -> Generator[tuple[str, TextIOWrapper], Any, None]:
        for file in os.listdir("sessions"):
            session_path = os.path.join(self.path, file)
                
            try:
                if file.endswith(".jsession"):
                    with open(session_path, "r") as file:
                        data = json.load(file)

                    yield session_path, data

            except Exception as error:
                console.print("Error : {}".format(error))