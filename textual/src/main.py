import dagger
from dagger.mod import Annotated, Doc, function

VERSION = "0.41.0"
VERSION_TYPE = Annotated[str, Doc("The textual version to install")]



@function(name="list")
async def list_(version: VERSION_TYPE = VERSION) -> str:
    """List all examples in the textual repository."""
    return await (
        base(version)
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
    name: Annotated[str, Doc("The name of the example to run")],
    version: VERSION_TYPE = VERSION,
) -> dagger.Container:
    """Run a textual example."""
    return (
        base(version)
        .with_entrypoint(["python", f"{name}.py"])
    )


def examples(version: str) -> dagger.Directory:
    return (
        dagger
        .git("https://github.com/Textualize/textual.git")
        .tag(f"v{version}")
        .tree()
        .directory("examples")
    )


def base(version: str) -> dagger.Container:
    cache_key = "pipcache-py312-alpine-daggerverse-textual"
    return (
        dagger.container()
        .from_("python:3.12-alpine")
        .with_mounted_cache("/root/.cache/pip", dagger.cache_volume(cache_key))
        .with_exec(["pip", "install", f"textual=={version}"])
        .with_mounted_directory("/src", examples(version))
        .with_workdir("/src")
    )
