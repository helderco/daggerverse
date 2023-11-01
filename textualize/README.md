# Dagger module for Textualize examples.

This module is meant to test Dagger's capabilities in rendering these
rich TUI libraries from [Textualize](https://github.com/Textualize).

[Rich](https://github.com/Textualize/rich) is a library for rich text
and beautiful formatting in the terminal.

[Textual](https://github.com/Textualize/textual) is a Python framework
for building terminal applications.


## Commands

### List

To list the available examples:

```shell
dagger call rich list
✔ dagger call rich list [2.96s]
┃ attrs
┃ bars
┃ columns
┃ cp_progress
┃ downloader
┃ dynamic_progress
┃ exception
┃ export
┃ file_progress
┃ fullscreen
┃ group
┃ group2
┃ highlighter
┃ jobs
┃ justify
┃ justify2
┃ layout
┃ link
┃ listdir
┃ live_progress
┃ log
┃ overflow
┃ padding
┃ print_calendar
┃ rainbow
┃ recursive_error
┃ repr
┃ save_table_svg
┃ screen
┃ spinners
┃ status
┃ suppress
┃ table
┃ table_movie
┃ top_lite_simulator
┃ tree
• Engine: 5e941878e6ae (version devel ())
⧗ 19.95s ✔ 210 ∅ 4
```

Or textual:

```shell
dagger call textual list
✔ dagger call list [6.59s]
┃ calculator
┃ code_browser
┃ color_command
┃ dictionary
┃ five_by_five
┃ json_tree
┃ markdown
┃ pride
• Engine: 9612a33e277a (version v0.9.2)
⧗ 14.00s ✔ 174 ∅ 16
```

### Demo

To run a demo from the list:

```shell
dagger shell textual demo --name json_tree
```

Some examples need arguments but `dagger shell` doesn't show that output.
You can use `dagger call` for that though:

```shell
dagger call rich demo --name downloader
✔ dagger call rich demo [2.28s]
┃ Usage:
┃         python downloader.py URL1 URL2 URL3 (etc)
• Engine: 5e941878e6ae (version devel ())
⧗ 10.68s ✔ 200 ∅ 21
```
