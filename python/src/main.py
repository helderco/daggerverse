import dagger
from dagger.mod import Annotated, Arg, Doc, function, object_type

PYTHON_VERSION= "3.12"


@function
def http_server(
    src: dagger.Directory,
    bind: Annotated[
        int,
        Doc("Bind to this backend port"),
    ] = 8000,
    version: Annotated[
        str,
        Doc("Use this Python version"),
        Arg("python_version")
    ] = PYTHON_VERSION,
) -> dagger.Service:
    """Start an HTTP server on a directory."""
    return (
        dagger.container()
        .from_(f"python:{version}-alpine")
        .with_mounted_directory("/srv", src)
        .with_workdir("/srv")
        .with_exec(["python", "-m", "http.server", str(bind)])
        .with_exposed_port(bind)
        .as_service()
    )


@object_type
class Sphinx:
    version: str = "7.2.6"
    python_version: str = PYTHON_VERSION

    def base(self) -> dagger.Container:
        return (
            dagger.container()
            .from_(f"python:{self.python_version}-alpine")
            .with_exec(["pip", "install", f"sphinx=={self.version}"])
            .with_workdir("/work")
        )

    @function
    def quickstart(
        self,
        project: Annotated[str, Doc("Project name")] = "Sphinx Demo",
        author: Annotated[str, Doc("Author name")] = "Dagger @ KubeCon NA 2023",
    ) -> dagger.Directory:
        """Create and build a new Sphinx project."""

        src = (
            self.base()
            .with_exec([
                "sphinx-quickstart", "-q",
                # Project and author are required flags.
                "-p", project,
                "-a", author,
                ".",
            ])
            .directory(".")
            .without_file("Makefile")
            .without_file("make.bat")
        )

        return (
            dagger.directory()
            .with_directory("docs", src)
            .with_directory("public", self.build(src))
        )

    @function
    def build(self, src: dagger.Directory) -> dagger.Directory:
        """Generate HTML documentation from source files."""
        return (
            self.base()
            .with_mounted_directory("/src", src)
            .with_exec(["sphinx-build", "/src", "."])
            .directory(".")
        )

    @function
    def preview(self, src: dagger.Directory) -> dagger.Service:
        """Build and preview documentation in a browser."""
        return http_server(self.build(src))


@function
def sphinx(version: Annotated[str | None, Doc("Sphinx version")] = None) -> Sphinx:
    """Create and build documentation with Sphinx."""
    kwargs = {}
    if version is not None:
        kwargs["version"] = version
    return Sphinx(**kwargs)
