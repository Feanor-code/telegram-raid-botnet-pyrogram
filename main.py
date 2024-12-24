import asyncio
import os
from sys import exit
from typing import Any

from rich.console import Console

from core.module_manager import Manager
from utils.registration import Registration
from utils.session_settings import SessionSettings


console = Console()
manager = Manager()
session_settings = SessionSettings()


if not os.path.exists("config.toml"):
    Registration().get_settings()
    exit()

console.print(
    "Pyrogram botnet: https://github.com/Feanor-code/telegram-raid-botnet-pyrogram",
    "Telethon botnet: https://github.com/json1c/telegram-raid-botnet",
    sep="\n",
    style="bold white"
)

print()

async def get_function() -> tuple[type[Any], bool | None]:
    initialized = await session_settings.ask("sessions")
    functions = manager.get_functions("modules")

    console.print(
        "[bold white]Accounts: {}"
        .format(len(session_settings.sessions))
    )

    for index, function in enumerate(functions, 1):
        console.print(
            "[bold magenta][{}][/] [bold white]{}".format(index, function.__doc__)
        )

    print()    
    return functions[int(console.input("[bold white]> "))-1], initialized


async def main() -> None:
    function, initialized = await get_function()
    
    await manager.manage_tasks(
        function(),
        True if console.input("[white]Async function? (y/n): ") == "y" else None,
        session_settings.sessions,
        initialized
    )
    await session_settings.stop_sessions()


while True:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        console.print("\n<https://sower.space>")
        break
    except Exception as error:
        console.print(error)
    finally:
        print("Done.")
