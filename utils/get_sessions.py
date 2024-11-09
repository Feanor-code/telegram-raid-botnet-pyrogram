import os


def get_sessions(path: str = "sessions") -> list[str]:
    return [file for file in os.listdir(path) if file.endswith(".")]