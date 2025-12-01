from pathlib import Path
from rich import print as rprint
from rich.prompt import Prompt


def info(message: str) -> None:
    rprint(f"[bold cyan]{message}[/]")


def success(message: str) -> None:
    rprint(f"✅[bold green] {message}[/]")


def warn(message: str) -> None:
    rprint(f"⚠️[bold yellow]  {message}[/]")


def error(message: str) -> None:
    rprint(f"❌[bold red] {message}[/]")


def print_verbose(message: object) -> None:
    rprint(f"[yellow]{message}[/]")


def print_duplicates(duplicate_results: list[Path]) -> None:
    for f in duplicate_results:
        rprint(f"[grey54] - {f}[/]")


def ask_yes_no(prompt: str, style: str) -> bool:
    return (
        Prompt.ask(
            f"[{style}]{prompt}[/]", choices=["Y", "N"], case_sensitive=False
        ).lower()
        == "y"
    )
