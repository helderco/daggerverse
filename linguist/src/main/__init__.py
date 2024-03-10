"""A tool for analyzing the languages used in a git repository

Mostly used for confirming that a .gitattributes file correctly marks a given
file as being generated.

Note: there's an issue when cache is cold. The linguist repo is pulled with
dag.git() which also pulls in the submodules. Every language in Linguist is
in an external repo, commited as a submodule, so it takes approximately 10
minutes to pull the entire thing.
"""
from typing import Annotated, Final

import dagger
from dagger import Doc, dag, field, function, object_type

REPO: Final[str] = "github.com/github-linguist/linguist"
DEFAULT_COMMIT: Final[str] = "559a6426942abcae16b6d6b328147476432bf6cb"


@object_type
class Linguist:
    """Build Linguist and analyze a git repository"""

    src: Annotated[
        dagger.Directory,
        Doc("The directory containing the source code to analyze"),
    ] = field()

    repo: Annotated[
        str,
        Doc("The Linguist GitHub repository to build"),
    ] = field(default=REPO, init=False)

    commit: Annotated[
        str,
        Doc("The Git commit for the Linguist repository to use"),
    ] = field(default=DEFAULT_COMMIT)

    @function
    async def run(
        self,
        file: Annotated[str, Doc("Path to a single file to analyze")] = "",
        *,
        rev: Annotated[str, Doc("The git revision to analyze")] = "",
        breakdown: Annotated[bool, Doc("Show the breakdown of files by language")] = False,
        as_json: Annotated[bool, Doc("Output the Linguist data in JSON format")] = False,
    ) -> str:
        """Run the github-linguist tool on the source code"""
        args = ["github-linguist"]
        if rev:
            args += ["--rev", rev]
        if breakdown:
            args += ["--breakdown"]
        if as_json:
            args += ["--json"]
        if file:
            args += [file]
        return await (
            dag.git(self.repo, keep_git_dir=True)
            .commit(self.commit)
            .tree()
            .docker_build()
            .with_mounted_directory("/mnt", self.src)
            .with_workdir("/mnt")
            .with_exec(args)
            .stdout()
        )
