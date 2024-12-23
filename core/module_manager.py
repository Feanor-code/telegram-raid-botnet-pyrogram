import asyncio
import inspect
import importlib.util
import os
import time
from itertools import islice
from typing import Generator, Any

from pyrogram import Client
from rich.console import Console
from rich.prompt import Prompt

from utils.session_settings import SessionSettings
from utils.update import get_commit


console = Console()


class Manager(SessionSettings):
    def __init__(self) -> None:
        get_commit()

    def load_functions(self, path: str, functions: list) -> Generator[type[Any], Any, None]:
        for function in functions:
            try:
                function = importlib.import_module(f"{path}.{function}")
                for _, classobj in inspect.getmembers(function, inspect.isclass):
                    if path in classobj.__module__ and not classobj.__doc__ is None:
                        yield classobj

            except Exception as error:
                console.log("Error : {}".format(error), style="bold")

    def get_functions(self, path: str) -> list[type[Any]]:
        return list(
            dict.fromkeys(
                self.load_functions(
                    path, 
                    sorted([
                        file[:-3] for file in os.listdir(path) if file.endswith(".py")
                    ])
                )
            )
        )

    async def manage_tasks(
        self, 
        function: Any, 
        is_sync: bool | None,
        sessions: dict[str, Client],
        initialized: bool
    ) -> None:
        self.initialized = initialized
        if await function.ask() == True:
            return

        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use?",
            default=str(len(sessions))
        ))
        sessions = dict(islice(sessions.items(), accounts_count))

        if is_sync is not None:
            await self._execute_async(sessions, function)
            
            if hasattr(function, "prt"):
                function.prt()
            
            return

        await self._execute_sync(sessions, function)

    async def _execute_sync(self, sessions: dict[str, Client], function: Any) -> None:
        for session in sessions.values():
            await self._execute(session, function)

    async def _execute_async(self, sessions: dict[str, Client], function: Any) -> None:
        start_time = time.perf_counter()
        
        await asyncio.gather(*[
            self._execute(session, function)
            for session in sessions.values()
        ])

        end_time = round(time.perf_counter() - start_time, 2)
        
        console.print(
            "[*] {used} bots used. Time: [yellow]{last_time}[/]s"
            .format(used=len(sessions), last_time=end_time)
        )   

    async def _execute(self, session: Client, function: Any) -> None:
        if not self.initialized or session.is_connected is None:
            session: Client | None = await self.launch(session)
        
        await function.execute(session)