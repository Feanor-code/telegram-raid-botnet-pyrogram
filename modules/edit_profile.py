import asyncio
import random

from pyrogram import Client
from rich.console import Console
from rich.prompt import Confirm

from modules.base.base import BaseFunction 
from utils.storage_settings import Settings


console = Console()


class EditProfile(BaseFunction, Settings):
    """Edit bio/name"""

    async def ask(self) -> None:
        is_from_config = True if console.input("[white]Use names from [green]config.toml[/]? (y/n): ") == "y" else None

        if is_from_config is None:
            self.first_names = self.parse_comma_separated("[bold red]Enter first names: ")

        self.last_names = self.parse_comma_separated("[bold red]Enter last names (Enter if not needed): ")
        self.bio = console.input("[bold red]Bio (Enter if not needed): ")

    async def execute(self, session: Client) -> None:
        try:
            new_first_name = random.choice(self.first_names)
            new_last_name = None if not self.last_names else random.choice(self.last_names)
            me = await session.get_me()

            if not await session.update_profile(
                first_name=new_first_name,
                last_name=new_last_name,
                bio=self.bio
            ):
                return console.print(f"Failed to change account name. {session.name}")
            
            console.print(
                "[*] First name {old_name} changed to {new_name}"
                .format(old_name=me.first_name, new_name=new_first_name)
            )
        except Exception as error:
            console.print(
                "{name} Account cannot edit profile. Error : {error}"
                .format(name=session.name, error=error)
            )