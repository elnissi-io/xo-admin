import asyncio
import functools
from typing import Callable

import click

from xoadmin.cli.utils import render


def output_format(func: Callable) -> Callable:
    """Decorator to handle output format."""

    @click.option(
        "--format",
        "format_",
        type=click.Choice(["yaml", "json"], case_sensitive=False),
        default="yaml",
        help="Output format.",
    )
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)
        format_ = kwargs.get(
            "format_", "yaml"
        )  # Get the format from the command options
        return render(result, format_)

    return wrapper
