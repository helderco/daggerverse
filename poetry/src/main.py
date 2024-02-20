"""Minimal Python example using the Poetry package manager.

This examples demostrates how any package manager that supports
pyproject.toml with a build backend (PEP 517) naturally works with
Dagger.

Python modules are installed with `pip install .` by the runtime container.
As long as a `main` package is installed in a way that's importable with
`import main`, it should work with Dagger.
"""
from typing import Annotated

import dagger
from dagger import Doc, dag, function, object_type


@object_type
class Poetry:
    """Main object type for this module."""

    @function
    def container_echo(
        self,
        string_arg: Annotated[str, Doc("The string to echo")],
    ) -> dagger.Container:
        """Echo a string in an alpine container."""
        # Example usage: "dagger call container-echo --string-arg hello"
        return dag.container().from_("alpine").with_exec(["echo", string_arg])


    @function
    async def grep_dir(
        self,
        directory_arg: Annotated[dagger.Directory, Doc("The directory to search in")],
        pattern: Annotated[str, Doc("The pattern to search for")],
    ) -> str:
        """Find a pattern in a directory."""
        # Example usage: "dagger call grep-dir --directory-arg . --patern grep_dir"
        return await (
            dag.container()
            .from_("alpine")
            .with_mounted_directory("/mnt", directory_arg)
            .with_workdir("/mnt")
            .with_exec(["grep", "-R", pattern, "."])
            .stdout()
        )
