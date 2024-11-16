from pyrogram import Client
from rich.console import Console


console = Console()


class SetPassword:
    """Enable 2fa on your account"""

    async def ask(self) -> None:
        self.password = console.input("[bold red]Password> [/]")

    async def execute(self, session: Client) -> None:
        try:
            me = await session.get_me()
            await session.enable_cloud_password(self.password)

        except Exception as error:
            console.print(f"[bold]The password is not set.[red] Error: {error}[/]")

        else:
            console.print(f"[bold green]{me.first_name} - the password is set.[/]")
