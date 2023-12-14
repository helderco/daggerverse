from typing import Annotated

from dagger import function


@function
def hello(name: Annotated[str, "The name of the person to say hello to."]) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"
