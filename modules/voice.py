import os

from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream

from pyrogram import Client
from pyrogram.types import User
from rich.console import Console

from modules.base.base import BaseFunction


console = Console()


class Voice(BaseFunction):
    """Voice chat raid"""

    async def ask(self) -> None:
        self.link = await self.change_link(console.input("[bold red]link(or ID)> "))
        files = os.listdir(os.path.join("resources", "voice"))

        if not files:
            return console.print("[bold red]Add video or audio!")
        
        for index, file in enumerate(files):
            console.print(
                "[{index}] {name}"
                .format(index=index+1, name=file)
            )

        self.media_file = files[int(console.input("[bold white]>> "))-1]

    async def voice_raid(self, session: Client, me: User, chat_id: int) -> None:
        app = PyTgCalls(session)
        
        await app.start()
        console.print(
            "[bold white][*] ({name}) [green]{file}"
            .format(name=me.first_name, file=self.media_file)
        )
        await app.play(
            chat_id,
            MediaStream(
                media_path=os.path.join(
                    "resources", "voice", self.media_file
                )
            )
        )
        await idle()

    async def execute(self, session: Client) -> None:
        try:
            me = await session.get_me()
            chat = await session.get_chat(self.link)
            
            await self.voice_raid(session, me, chat.id)
        except Exception as error:
            return console.print(
                f"Account will not join voice chat. Error : {error}"
            )