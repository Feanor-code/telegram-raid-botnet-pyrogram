import asyncio
from dataclasses import dataclass, field
import json
import os

from pyrogram import Client
from rich.console import Console
from rich.prompt import Prompt


console = Console()


@dataclass
class SessionSettings:
    sessions: dict[str, Client] = field(default_factory=dict)

    async def ask(self, path: str):
        for file in os.listdir(path):
            if file.endswith(".session"):
                session_path = os.path.join(path, file)
                
                with open(session_path) as file:
                    try:
                        session_data = json.load(file)
                    except Exception as error:
                        console.print(session_path, error, style="bold red")
                        continue
                
                session = Client(
                    name=session_path,
                    session_string=session_data["session"],
                    api_id=session_data["api_id"],
                    api_hash=session_data["api_hash"],
                    device_model=session_data["device_model"],
                    app_version=session_data["app_version"],
                    system_version=session_data["system_version"],
                    lang_code=session_data["lang_code"]
                )
                self.sessions[session.name] = session

        if len(self.sessions) == 0:
            return console.print(
                "[bold red]You need to add sessions (Telegram accounts)"
            )
        
        if is_sync := Prompt.ask("Initialize sessions?", choices=["y", "n"], default="n") == "y":
            with console.status("Connection..."):
                await asyncio.gather(*[
                    self.launch(session)
                    for session in self.sessions.values()
                ])
        
        return is_sync
        
    async def launch(self, session: Client):
        try:
            await session.start()
            console.log(f"Session {session.name} connected")
        except ConnectionError:
            pass
        
        except Exception as error:
            console.print(f"Session Path -> {session.name} [bold red]Error : {error}")
            self.sessions.pop(session.name)
            os.remove(session.name)
            return

        return session