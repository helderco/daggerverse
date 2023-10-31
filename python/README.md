# Dagger Python Module

[![dagger-min-version](https://img.shields.io/badge/dagger%20version-v0.9.2-green)](https://github.com/dagger/dagger/releases/tag/v0.9.2)

Easily manage Python tasks through Dagger.

## Before you start

Set `DAGGER_MODULE` to environment variable to avoid using
`-m github.com/helderco/daggerverse/python` in every command.

```shell
export DAGGER_MODULE=github.com/helderco/daggerverse/python
```

## Commands

### Run a HTTP server

The following will serve the files in the current directory:

```shell
dagger up http-server -n --src .
```

Open your browser on [http://0.0.0.0:8000](http://0.0.0.0:8000).
Click on the [dagger.html](http://0.0.0.0:8000/dagger.html) file.

### Create a new Sphinx project

```shell
dagger dl sphinx quickstart
````

This will populate by default the current directory with:
- `docs`: the Sphinx source files;
- `public`: the built documentation in HTML;


### Open the built documentation in the browser

```shell
dagger up http-server -n --src public
```

Open your browser on [http://0.0.0.0:8000](http://0.0.0.0:8000).

### Preview

You can build and preview the documentation with a single command,
without downloading the built files into your host.

Make some changes to the documentation source files and run:

```shell
dagger up sphinx preview -n --src docs
```

## Local development

You don't need to have Python in your host to run this module, but if you
want to edit the code it's helpful to get code inteligence in the IDE.

First, run codegen to get the SDK locally:

```shell
dagger mod sync
````

Create a virtual environment, activate it and install the SDK in
**editable** mode.

```shell
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
