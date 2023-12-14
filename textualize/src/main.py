from typing import Annotated

import dagger
from dagger import Doc, dag, function, object_type


@object_type
class Examples:
    package: str
    version: str

    @function(name="list")
    async def list_(self) -> str:
        """List all examples in the repository."""
        return await (
            self.base()
            .with_exec([
                "find", ".",
                "-maxdepth", "1",
                "-type", "f",
                "-name", "*.py",
                "-exec", "basename", "{}", ".py", ";",
            ])
            .stdout()
        )

    @function
    def demo(
        self,
        name: Annotated[
            str,
            Doc("The name of the example to run"),
        ],
        # TODO: cattrs has an issue with unions in Annotated. Fixed in main.
        arg: list[str] | None = None,
    ) -> dagger.Container:
        """Run an example."""
        arg = arg or []
        return (
            self.base()
            .with_entrypoint(["python"])
            .with_default_args(args=[f"{name}.py", *arg])
            .with_exec([])
        )

    def base(self) -> dagger.Container:
        cache_key = "pipcache-py312-alpine-daggerverse-textualize"
        return (
            dag.container()
            .from_("python:3.12-alpine")
            .with_mounted_cache("/root/.cache/pip", dag.cache_volume(cache_key))
            .with_exec(["pip", "install", f"{self.package}=={self.version}"])
            .with_mounted_directory("/src", self.examples_dir())
            .with_workdir("/src")
        )

    def examples_dir(self) -> dagger.Directory:
        return (
            dag
            .git(f"https://github.com/Textualize/{self.package}.git")
            .tag(f"v{self.version}")
            .tree()
            .directory("examples")
        )


@function
def rich(
    version: Annotated[str, Doc("The version of `rich` to install")] = "13.6.0",
) -> Examples:
    """Run `rich` examples."""
    return Examples(package="rich", version=version)


@function
def textual(
    version: Annotated[str, Doc("The version of `textual` to install")] = "0.41.0",
) -> Examples:
    """Run `textual` examples."""
    return Examples(package="textual", version=version)

