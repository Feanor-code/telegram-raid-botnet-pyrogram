from rich.console import Console
from directory_tree import display_tree
import toml
import os

console = Console()

path = "resources"

if not os.path.exists(path):
    os.mkdir(path)
    os.mkdir("sessions")

    folders = [
        "account_photo", 
        "photo", 
        "stickers", 
        "video", 
        "voice"
    ]
    
    for folder in folders:
        os.mkdir(os.path.join(path, folder))

    display_tree(path, header=True)

    print()

    console.print(
        "Folder \"resources\" create",
        "You can add resources.",
        sep="\n",
        style="bold yellow"
    )

    print()

class Registration:
    def get_settings(self) -> None:
        console.rule("Session")
        names = self.setup_session()

        console.rule("Flood")
        message_count, messages = self.setup_flood()

        self.save(
            message_count,
            messages,
            names
        )

    def setup_session(self) -> list[str]:
        console.print(
            "Enter account names",
            style="bold red"
        )

        names = []
        while name := console.input("[bold white]>> [/]"):
            names.append(name)      

        return names

    def setup_flood(self) -> tuple[int, list]:
        message_count = int(console.input("[bold yellow]Number of messages> [/]"))

        print()

        console.print(
            "Enter flood messages text",
            style="bold green"
        )

        messages = []
        while message := console.input("[bold white]>> [/]"):
            messages.append(message)

        return message_count, messages

    def save(
        self,
        message_count: int,
        messages: list,
        names: list
    ) -> None:
        config=dict(
            session=dict(
                names=names
            ),
            flood=dict(
                message_count=message_count,
                messages=messages
            )
        )

        with open("config.toml", "w") as file:
            toml.dump(config, file)

        console.rule("[bold white]Happy use! https://sower.space :)[/]")
        console.print("[bold white]Run the file again.[/]")
