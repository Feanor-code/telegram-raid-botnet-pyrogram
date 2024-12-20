import git
import pip

from rich.console import Console


console = Console()


def update():
    with console.status("Update..."):
        repo = git.Repo()

        try:
            origin = repo.remote("origin")
            origin.pull()
            pip.main([
                "install", 
                "-r", 
                "requirements.txt", 
                "--quiet", 
                "--break-system-packages"
            ])
        except git.exc.GitCommandError as error:
            console.print(error, style="yellow")
        except Exception as error:
            console.print(error, style="bold red")


def get_commit():
    with console.status("Checking for updates..."):
        try:
            repo = git.Repo()
            local_hash = repo.heads[0].commit.hexsha
            server_hash = git.Remote(repo, "origin").fetch()[0].commit.hexsha
        except Exception as error:
            return console.print(f"Error : {error}")
    
    if local_hash == server_hash:
        return console.print("The latest version is installed.")
    
    if console.input("[*] Update? (y/n): ") == "y":
        update()