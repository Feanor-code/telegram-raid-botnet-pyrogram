import toml


class Settings:
    def __init__(self) -> None:
        with open("config.toml", encoding="utf-8") as file:
            config = toml.load(file)

        self.first_names = config["session"]["names"]
        self.messages = config["flood"]["messages"]
        self.message_count = config["flood"]["message_count"]