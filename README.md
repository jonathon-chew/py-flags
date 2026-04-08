# Py Flags

## Summary
`py-flags` is a small Python project for defining and parsing command-line flags. I built it as a personal learning project to better understand class design, basic parsing logic, type conversion, validation, and unit testing.

## What This Project Demonstrates
- Python classes and object-oriented design
- storing CLI flag definitions and metadata
- parsing command-line style input into typed values
- handling defaults, required flags, and unknown flags
- writing unit tests for both success and failure cases

## Current Features
- define string, integer, and boolean flags
- support short and long flag names
- store helper text, types, and default values
- parse input into string, integer, and boolean values
- check whether a flag exists
- raise errors for unknown flags and missing required flags

## How To Run

You can experiment with the library directly from a Python session or from your own script by importing:

```python
from pyflags.flag import argument
```

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
import sys
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p", "--project"], helper="Project name", default="", required=True)
args.add_int(arguments=["--number"], helper="Build number", default=0)
args.add_bool(arguments=["--verbose"], helper="Enable verbose logging", default=False)

args.parse(sys.argv[1:])

print(args.get_value("--project"))
print(args.get_value("--number"))   # 3
print(args.get_value("--verbose"))  # True
```

Example command:

```bash
python3 app.py --project my-app --number 3 --verbose
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

### Get A Parsed Value

```python
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["--project"], helper="Project name", default="demo")

print(args.get_value("--project"))   # demo
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
import sys
from pyflags.flag import argument

args = argument()
args.add_string(arguments=["-p", "--project"], helper="Project name", default="", required=True)

args.parse(sys.argv[1:])
```

Example command:

```bash
python3 app.py --project my-app
```

## Testing

This project uses Python's built-in `unittest` module. The tests currently cover:
- flag creation for string, integer, and boolean values
- helper text and flag lookup behavior
- successful parsing for string, integer, and boolean flags
- failure cases such as unknown flags and missing required arguments

Run the full test suite with:

```bash
python3 -m unittest discover -s tests
```

## What I Learned

This project helped me get more comfortable with:
- designing a small but reusable class-based API
- separating flag registration from parsing logic
- converting string input into typed values safely
- using tests to catch parsing bugs and tighten up the design

## Next Improvements

- improve exception types and error messages
- handle more edge cases around invalid input
- support positional arguments and repeated flags
- refine the public API to make usage more intuitive
