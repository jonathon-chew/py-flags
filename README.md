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
- support string, integer, float, boolean, file, and list flags
- allow aliases to share the same underlying flag value
- support explicit `choices` for accepted values
- support custom validation functions for parsed values
- support custom parse hooks for advanced conversion
- support interactive prompting for missing required flags
- support one-call interactive parsing with `parse_and_resolve()`
- support optional prompting for missing values during script execution (`resolve()`)
- support inline `--flag=value` style input
- return a clean dictionary of parsed values with `get_flags()`
- get parsed values directly with `get_value()`
- support normalized attribute access such as `flags.project` and `flags.output_file`
- provide `get_optional()` and `resolve()` helpers for safer script flows
- raise errors for unknown flags and missing required flags

## Behavior Notes (Current)
- **Canonical name:** the *first* entry in `names=[...]` becomes the canonical name for that flag. Required flags are tracked by canonical name.
- **Aliases:** aliases share one flag object, but `get_flags()` returns entries for *each alias key* (so values are duplicated across aliases).
- **Required flags:** `parse()` does not fail at the end if required flags are missing; use `resolve_all()` (or call `get_value()` / `resolve()` on the missing flag) to surface missing-required errors.
- **Boolean flags:** providing a boolean flag token (e.g. `--verbose`) sets it to `True`. To explicitly set `False`, use equals syntax (e.g. `--verbose=false`). The split form `--verbose false` is not supported.
- **Boolean value strings:** equals syntax accepts `true/false`, `1/0`, `yes/no`, and `on/off`.
- **File flags:** file flags validate that the provided path exists at parse-time (and raise `FileNotFoundError` if it does not).
- **Attribute access:** registered flags can also be read through normalized dot access such as `flags.number` for `--number`.
- **List flags:** flags registered with `list` accumulate values across space-separated tokens and repeated uses of the same flag.

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
flags.add(names=["--project", "-p"], helper="Project name", value_type=str, default="demo")
flags.add(names=["--number", "-n"], helper="Build number", value_type=int, default=1)
flags.add(names=["--verbose"], helper="Enable verbose logging", value_type=bool, default=False)
flags.add_file(names=["--config", "-c"], helper="Path to config file")

print(flags.get_flags())
```

Example output:

```python
{"--project": "demo", "-p": "demo", "--number": 1, "-n": 1, "--verbose": False}
```

### Real Script Example

```python
import sys
from pyflags.flag import Flags

flags = Flags()
flags.add(["--project", "-p"], "Project name", str, required=True)
flags.add(["--env"], "Environment", str, choices=["dev", "test", "prod"])
flags.add(["--port"], "Server port", int, default=8000, validator=lambda value: 1 <= value <= 65535)
flags.add(["--tag"], "Tag", list)
flags.add_file(["--config", "-c"], "Config file", required=True)
flags.add(["--verbose"], "Enable verbose logging", bool, default=False)

flags.parse_and_resolve(sys.argv[1:])

project_name = flags.project
environment = flags.env
port = flags.get_optional("--port", 8000)
config_path = flags.config
tags = flags.tag

if flags.verbose:
    print(f"[verbose] Loading config from {config_path}")
    print(f"[verbose] Tags applied: {', '.join(tags)}")

print(f"Creating project: {project_name} in {environment} on port {port}")
```

Example command:

```bash
python3 app.py --env=prod --port=8080 --tag api tooling internal --verbose
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
./settings.json
[verbose] Loading config from settings.json
Creating project: my-app in prod on port 8080
```

In this flow:
- the script starts with `--env`, `--port`, and `--verbose`
- interactive mode notices `--project` and `--config` are missing
- the user enters `my-app` and `settings.json`
- the script collects `api`, `tooling`, and `internal` under `--tag`
- the script continues with the completed set of values

Note: because `--config` is a file flag, the path provided must exist when it is parsed/resolved.

If interactive mode is enabled, missing mandatory flags can be prompted for instead of immediately failing. That makes the parser useful for internal tools and setup scripts where a guided CLI experience is preferable to a hard stop.

You can also use the convenience wrapper:

```python
flags.parse_and_resolve(sys.argv[1:])
```

That enables interactive mode, parses the passed arguments, and then resolves any missing required flags in one call.

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
- `parse_and_resolve()` convenience behavior
- successful parsing for string, integer, boolean, and file flags
- accepted and rejected boolean string values in equals syntax
- accepted and rejected values enforced through `choices`
- custom validation for accepted and rejected values
- file-path validation for existing and missing files
- invalid integer and float conversions
- interactive prompting for missing required flags
- help output rendering
- normalized attribute access
- list accumulation behavior
- failure cases such as unknown flags and missing required arguments

Run the full test suite with:

```bash
python3 -m unittest discover -s tests
```

Or use the helper script:

```bash
bash tests/run_tests.sh
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
