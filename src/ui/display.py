from pathlib import Path
from rich import print as rprint
from rich.prompt import Prompt


def info(message: str, style: str | None = None) -> None:
    rprint(f"[bold {style} cyan]{message}[/]")


def success(message: str, style: str | None = None) -> None:
    rprint(f"✅[bold {style} green] {message}[/]")


def warn(message: str, style: str | None = None) -> None:
    rprint(f"⚠️[bold {style} yellow]  {message}[/]")


def error(message: str, style: str | None = None) -> None:
    rprint(f"❌[bold {style} red] {message}[/]")


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
