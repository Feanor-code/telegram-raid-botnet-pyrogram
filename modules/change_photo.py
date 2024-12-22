import os
import random
from typing import Literal

from pyrogram import Client
from rich.console import Console


console = Console()


class ChangePhoto:
    """Change profile photo"""

    async def ask(self) -> (Literal[True] | None):
        self.directory = os.path.join("resources", "account_photo/")
        self.files = os.listdir(self.directory)

        console.print(
            "[1] Set new photo",
            "[2] Delete all photos",
            sep="\n",
            style="bold white"
        )
        self.choice = int(console.input("[bold]>> "))-1

        if self.choice == 0 and not self.files:
            console.print(
                "[bold red][!][/] Add a photo for accounts.",
                f"Path: [yellow]{self.directory}",
                sep="\n"
            )
            return True

    async def change_photo(self, session: Client) -> (str | None):
        photo = self.directory+random.choice(self.files)
        
        if await session.set_profile_photo(photo=photo):
            return photo
            
    async def delete_photo(self, session: Client) -> None:
        async for photo in session.get_chat_photos("me"):
            await session.delete_profile_photos(photo.file_id)

    async def execute(self, session: Client) -> None:
        choices = (
            (
                self.change_photo, 
                "[bold green][+][/] Photo updated. ({name}) [yellow]{path}",
                "Photo not updated. Error : {error}"
            ),
            (
                self.delete_photo,
                "[bold green][-][/] Photo deleted. ({name})",
                "Photo not deleted. Error : {error}"
            )
        )
        try:
            me = await session.get_me()
            
            path = await choices[self.choice][0](session)
            console.print(
                choices[self.choice][1].format(
                    name=me.first_name,
                    path=path
                )
            )
        except Exception as error:
            console.print(choices[self.choice][2].format(error=error))