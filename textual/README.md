# Textual Dagger module

[Textual](https://github.com/Textualize/textual) is a Python framework
for building terminal applications.

This module is meant to test Dagger's capabilities in rendering these
advanced TUI manipulations.

## Commands

### List

To list the available examples:

```shell
dagger call list
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
dagger shell demo --name json_tree
```

