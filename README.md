# Py Flags

## Summary
Implement a simple command-line flag helper for defining and working with CLI arguments.

## What You'll Learn
- Python classes and objects
- methods and instance state
- dictionaries and lists for storing flag data
- basic CLI flag design and help output

## MVP
- define string, integer, and boolean CLI flags
- register flags and helper text
- print simple usage/help information
- simple CLI or library demo

## Stretch Goals
- parse command-line input
- validate required arguments
- support long and short flag names
- improve error messages and defaults

## Examples

### Define Some Flags

```python
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p", "--project"], helper="Project name", default="demo")
args.add_int(arguments=["-n", "--number"], helper="Build number", default=1)
args.add_bool(arguments=["--verbose"], helper="Enable verbose logging", default=False)
```

### Parse CLI Input

```python
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p"], helper="Project name", default="")
args.add_int(arguments=["--number"], helper="Build number", default=0)
args.add_bool(arguments=["--verbose"], helper="Enable verbose logging", default=False)

args.parse(["-p", "my-app", "--number", "3", "--verbose"])

flags = args.get_flags()

print(flags["-p"].value)         # my-app
print(flags["--number"].value)   # 3
print(flags["--verbose"].value)  # True
```

### Check Whether A Flag Exists

```python
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p", "--project"], helper="Project name", default="")

print(args.check_flag("-p"))         # True
print(args.check_flag("--project"))  # True
print(args.check_flag("--missing"))  # False
```

### Show Help Text

```python
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p"], helper="Project name", default="demo")
args.add_bool(arguments=["--verbose"], helper="Enable verbose logging", default=False)

args.helper()
```

### Required Flag Example

```python
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p"], helper="Project name", default="", required=True)

args.parse(["-p", "my-app"])
```
