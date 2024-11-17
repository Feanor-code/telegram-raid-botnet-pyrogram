import asyncio
import os
from sys import platform, exit

from rich.console import Console

from core.module_manager import Manager
from utils.registration import Registration
from utils.session_settings import SessionSettings


console = Console()
manager = Manager()
session_settings = SessionSettings()


if platform == "win32":
    console.print("[bold red]The script will work with errors (use linux or WSL).")

if not os.path.exists("config.toml"):
    Registration().get_settings()
    exit()

console.print(
    "GitHub botnet on pyrogram: https://github.com/Feanor-code/telegram-raid-botnet-pyrogram",
    "GitHub botnet on telethon: https://github.com/json1c/telegram-raid-botnet",
    sep="\n",
    style="bold white"
)

print()

async def get_function():
    await session_settings.ask("sessions")
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
    
    return functions[int(console.input("[bold white]> "))-1]

async def main():
    function = await get_function()
    is_sync = True if console.input("Async function? (y/n): ") == "y" else None
    
    await manager.manage_tasks(
        function(),
        is_sync,
        session_settings.sessions
    )


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
