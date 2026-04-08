# Py Flags

## Summary
`py-flags` is a small Python project for defining and parsing command-line flags. I built it as a personal learning project to better understand class design, basic parsing logic, type conversion, validation, and unit testing.

## What This Project Demonstrates
- Python classes and object-oriented design
- storing CLI flag definitions and metadata
- modelling aliases as one logical flag with multiple names
- parsing command-line style input into typed values
- handling defaults, required flags, and unknown flags
- writing unit tests for both success and failure cases

## Current Features
- define string, integer, and boolean flags
- support short and long flag names
- allow aliases to share the same underlying flag value
- store helper text, types, and default values
- parse input into string, integer, and boolean values
- check whether a flag exists
- get parsed values directly with `get_value()`
- raise errors for unknown flags and missing required flags

## How To Run

You can experiment with the library from a Python session or your own script by importing:

```python
from pyflags.flag import Flags
```

## Examples

### Define Some Flags

```python
from pyflags.flag import Flags

flags = Flags()
flags.add(names=["-p", "--project"], helper="Project name", type=str, default="demo")
flags.add(names=["-n", "--number"], helper="Build number", type=int, default=1)
flags.add(names=["--verbose"], helper="Enable verbose logging", type=bool, default=False)
```

### Real Script Example

```python
import sys
from pyflags.flag import Flags

flags = Flags()
flags.add(["--project", "-p"], "Project name", str, required=True)
flags.add(["--verbose"], "Enable verbose logging", bool, default=False)

flags.parse(sys.argv[1:])

project_name = flags.get_value("--project")

if flags.get_value("--verbose"):
    print(f"[verbose] Starting project setup for {project_name}")

print(f"Creating project: {project_name}")
```

Example command:

```bash
python3 app.py --project my-app --verbose
```

Example output:

```text
[verbose] Starting project setup for my-app
Creating project: my-app
```

### Alias Example

```python
import sys
from pyflags.flag import Flags

flags = Flags()
flags.add(["--project", "-p"], "Project name", str, required=True)

flags.parse(sys.argv[1:])

print(flags.get_value("--project"))  # my-app
print(flags.get_value("-p"))         # my-app
```

Example command:

```bash
python3 app.py -p my-app
```

## Testing

This project uses Python's built-in `unittest` module. The tests currently cover:
- flag creation for string, integer, and boolean values
- helper text and flag lookup behavior
- generic `add(...)` behavior and shared alias objects
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
- handling aliases through a canonical flag model
- converting string input into typed values safely
- using tests to catch parsing bugs and tighten up the design

## Next Improvements

- improve exception types and error messages
- handle more edge cases around invalid input
- support positional arguments and repeated flags
- continue polishing naming and API ergonomics
