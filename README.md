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
- support string, integer, float, boolean, and file flags
- allow aliases to share the same underlying flag value
- support explicit `choices` for accepted values
- support custom validation functions for parsed values
- support custom parse hooks for advanced conversion
- support interactive prompting for missing required flags
- support optional prompting for missing values during script execution (`resolve()`)
- support inline `--flag=value` style input
- return a clean dictionary of parsed values with `get_flags()`
- get parsed values directly with `get_value()`
- provide `get_optional()` and `resolve()` helpers for safer script flows
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
flags.add(names=["-p", "--project"], helper="Project name", value_type=str, default="demo")
flags.add(names=["-n", "--number"], helper="Build number", value_type=int, default=1)
flags.add(names=["--verbose"], helper="Enable verbose logging", value_type=bool, default=False)
flags.add_file(names=["--config", "-c"], helper="Path to config file")

print(flags.get_flags())
```

Example output:

```python
{"-p": "demo", "--project": "demo", "-n": 1, "--number": 1, "--verbose": True, "--config": ""}
```

### Real Script Example

```python
import sys
from pyflags.flag import Flags

flags = Flags()
flags.activate_interactive_mode()
flags.add(["--project", "-p"], "Project name", str, required=True)
flags.add(["--env"], "Environment", str, choices=["dev", "test", "prod"])
flags.add(["--port"], "Server port", int, default=8000, validator=lambda value: 1 <= value <= 65535)
flags.add_file(["--config", "-c"], "Config file", required=True)
flags.add(["--verbose"], "Enable verbose logging", bool, default=False)

flags.parse(sys.argv[1:])

project_name = flags.get_value("--project")
environment = flags.get_value("--env")
port = flags.get_optional("--port", 8000)
config_path = flags.get_value("--config")

if flags.get_value("--verbose"):
    print(f"[verbose] Loading config from {config_path}")

print(f"Creating project: {project_name} in {environment} on port {port}")
```

Example command:

```bash
python3 app.py --env=prod --port=8080 --verbose
```

Example interactive session:

```text
--project (str) is required.
Project name
Type: <class 'str'>
Default Value is set as: None
my-app
--config (Path) is required.
Config file
Type: <class 'pathlib.Path'>
Default Value is set as: None
settings.json
[verbose] Loading config from settings.json
Creating project: my-app in prod on port 8080
```

In this flow:
- the script starts with `--env`, `--port`, and `--verbose`
- interactive mode notices `--project` and `--config` are missing
- the user enters `my-app` and `settings.json`
- the script continues with the completed set of values

If interactive mode is enabled, missing mandatory flags can be prompted for instead of immediately failing. That makes the parser useful for internal tools and setup scripts where a guided CLI experience is preferable to a hard stop.

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

## Why This Is Different

Many popular Python CLI parsers focus on declaration and immediate failure. This project experiments with a more guided workflow:
- shared alias handling through one logical flag object
- validation layers with `choices`, custom validators, and file-path checks
- interactive recovery for missing required flags instead of always exiting immediately
- helper methods like `get_optional()` and `resolve()` for safer script-level usage

That combination makes it useful not just for strict CLIs, but also for lightweight internal tools and guided scripts.

## Testing

This project uses Python's built-in `unittest` module. The tests currently cover:
- flag creation for string, integer, and boolean values
- helper text and flag lookup behavior
- generic `add(...)` behavior and shared alias objects
- value-facing `get_flags()` and `get_value()` behavior
- safer access patterns through `get_optional()` and `resolve()`
- inline `--flag=value` parsing
- successful parsing for string, integer, boolean, and file flags
- accepted and rejected values enforced through `choices`
- custom validation for accepted and rejected values
- file-path validation for existing and missing files
- interactive prompting for missing required flags
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
- separating user-facing return values from internal flag objects
- validating file paths during parsing
- adding constrained inputs through `choices`
- adding custom validators after type conversion
- exploring interactive recovery for missing required inputs
- converting string input into typed values safely
- using tests to catch parsing bugs and tighten up the design

## Next Improvements

- improve exception types and error messages
- handle more edge cases around invalid input
- support positional arguments and repeated flags
