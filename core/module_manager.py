import asyncio
import os
import inspect
import importlib.util
from typing import Generator, Any

from pyrogram import Client
from rich.console import Console

from utils.session_settings import SessionSettings


console = Console()


class Manager(SessionSettings):
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
            self.load_functions(
                path, 
                sorted([
                    file[:-3] for file in os.listdir(path) if file.endswith(".py")
                ])
            )
        )

    async def manage_tasks(
        self, 
        function: Any, 
        is_sync: bool | None,
        sessions: dict[str, Client]
    ) -> None:
        data: tuple = await function.ask()

        if is_sync is not None:
            return await self._execute_async(sessions, function, data)

        await self._execute_sync(sessions, function, data)

    async def _execute_sync(self, sessions: dict[str, Client], function: Any, data: tuple) -> None:
        for session in sessions.values():
            await self._execute(session, function, data)

    async def _execute_async(self, sessions: dict[str, Client], function: Any, data: tuple) -> None:
        await asyncio.gather(
            *(
                self._execute(session, function, data)
                for session in sessions.values()
            )
        )

    async def _execute(self, session: Client, function: Any, data: tuple) -> None:
        session: Client = await self.launch(session)

        if await function.execute(
            session,
            data
        ):
            await session.stop()