import asyncio
from sys import exit, platform

from rich.console import Console

from core.module_manager import Manager
from utils.sessions_settings import SessionsSettings


console = Console()
manager = Manager()
session_settings = SessionsSettings("sessions")


if platform == "win32":
    console.print("[bold red]The script will work with errors (use linux or WSL).")

console.print(
    "GitHub botnet on pyrogram: https://github.com/Madara225/telegram-raid-botnet-pyrogram",
    "GitHub botnet on telethon: https://github.com/json1c/telegram-raid-botnet",
    sep="\n",
    style="bold white"
)

print()

def main():
    session_settings.ask()
    functions = manager.get_functions("modules")

    console.print("[bold white]Accounts: {}".format(50))

    for index, function in enumerate(functions, 1):
        console.print(
            "[bold magenta][{}] [white]{}".format(index, function.__doc__)
        )

    print()
    
    return functions[int(console.input("[bold white]> "))-1]


while True:
    try:
        function = main()
        is_sync = True if console.input("Async function? (y/n): ") == "y" else None
        
        asyncio.run(
            manager.manage_tasks(
                function(),
                is_sync
            )
        )

    except KeyboardInterrupt:
        console.print("\n<https://sower.space>")
        exit()

    except Exception as error:
        console.print(error)

    finally:
        print("Done.")
