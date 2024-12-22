import asyncio
import os
import random

from pyrogram import Client, enums
from pyrogram.errors.exceptions import FloodWait, SlowmodeWait
from pyrogram.types import User
from rich.console import Console
from rich.prompt import Confirm

from modules.base.base import BaseFunction
from utils.storage_settings import Settings


console = Console()


class Flood(BaseFunction, Settings):
    """Flood chat"""

    def __init__(self) -> None:
        super().__init__()
        self.choices = (
            ("Raid text", self.flood_text),
            ("Raid photo", self.flood_photo)
        )

    async def ask(self, inside: bool | None = None) -> None:
        print()

        for index, function in enumerate(self.choices, 1):
            console.print(
                "[bold white][{index}] {name}"
                .format(index=index, name=function[0])
            )

        self.mode = self.choices[int(console.input("[bold]> "))-1][1]
        self.notify_all = Confirm.ask("[bold red]notify all?", default="y")

        if self.notify_all:
            self.notify_admin = Confirm.ask("[bold red]notify admin?", default="y")

        if inside is None:
            self.link = await self.change_link(
                console.input("[bold red]link(or ID)> ")
            )
        await self.delay(ask=True)

    async def flood_text(self, session: Client, chat_id: int, text: str) -> None:
        await session.send_message(chat_id, text)

    async def flood_photo(self, session: Client, chat_id: int, _) -> None:
        file = random.choice(os.listdir(os.path.join("resources", "photo")))

        await session.send_photo(
            chat_id,
            os.path.join(
                "resources", "photo", 
                file
            )
        )

    async def get_users(self, session: Client, chat_id: int) -> list[int]:
        users_id = []
        async for user in session.get_chat_members(chat_id):
            if user.status in [
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR
            ] and not self.notify_admin:
                continue

            users_id.append(user.user.id)
        return users_id

    async def flood(
        self, 
        session: Client,
        me: User,
        chat_id: int,
        users_id: list[int]
    ) -> None:
        successes = 0
        errors = 0

        while successes < self.message_count:
            if not self.notify_all:
                message = random.choice(self.messages)
            else:
                message = "<a href=\"tg://user?id={user_id}\">\u206c\u206f</a>{message}" \
                .format(
                    user_id=random.choice(users_id),
                    message=random.choice(self.messages)
                )
            try:
                await self.mode(session, chat_id, message)
            except (FloodWait, SlowmodeWait) as wait:
                wait = wait.value

                console.print(f"[bold red]Wait {wait} seconds!")
                await asyncio.sleep(wait)

            except Exception as error:
                errors += 1
                console.print(f"[bold red]Message not Sent. Error : {error}")
            
            else:
                successes += 1
                console.print(
                    "({name}) [bold green]sent[/] COUNT: [magenta]{count}"
                    .format(name=me.first_name, count=successes)
                )

            finally:
                if errors >= 3:
                    return await session.leave_chat(chat_id, delete=True)
                
                await self.delay()

    async def execute(self, session: Client) -> None:
        try:
            me = await session.get_me()
            chat = await session.get_chat(self.link)

            if self.notify_all:
                users_id = await self.get_users(session, chat.id)

            await self.flood(
                session, 
                me,
                chat.id,
                users_id
            )
        except Exception as error:
            return console.print(f"Messages will not be sent. Error : {error}")
        