# Minimal Poetry Dagger module

This is a minimal example of replacing the generated `pyproject.toml`
from `dagger mod init` to Poetry.

## Caveats

### Local development

For local development, you'll need to run `dagger mod sync` to update the
SDK locally. It should only be needed if you don't have it already (it's
in `.gitignore`), if you upgrade Dagger, or if you change the module's
dependencies.

After that just do a `poetry install` to install the SDK as an editable
dependency locally to get code intelligence in your IDE. You should
repeat it when upgrading Dagger as it may contain different requirements.

### Pinned dependencies

Lock files aren't supported yet, so if you need to pin a dependency
you'll need to do that in `pyproject.toml` for now. `poetry.lock` will
be ignored when executing the module's functions.

In Dagger, the module will be installed by `pip install .`, which is possible
due to [PEP-517](https://python-poetry.org/docs/pyproject/#poetry-and-pep-517),
so anything Poetry specific won't work in the runtime container.

### Project name

At least for now, the SDK expects a module called `main` to be installed
in `site-packages`. Poetry defaults to finding packages under `./src` with
the same name as the Poetry project. If you choose to change that name,
then you need to [tell Poetry where to find](https://python-poetry.org/docs/pyproject/#packages) the module:

```toml
packages = [{ include = "main.py", from = "src" }]
```

If you have multiple files, you can turn `main.py` into a package
(`./src/main/__init__.py`):

```toml
packages = [{ include = "main", from = "src" }]
```

