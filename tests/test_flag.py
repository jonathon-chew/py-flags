import unittest
import json
import io
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from pyflags.flag import Flags
from typing import Any


class TestArgument(unittest.TestCase):
    def setUp(self):
        self.args = Flags()

    def test_add_creates_string_flag(self):
        self.args.add(
            names=["-p"],
            helper="Project name",
            value_type=str,
            default="pyflag",
        )

        flags = self.args.get_flags()

        self.assertIn("-p", flags.keys())
        self.assertEqual(flags["-p"], "pyflag")
        self.assertIsInstance(flags["-p"], str)

    def test_add_aliases_share_the_same_flag_object(self):
        self.args.add(
            names=["--project", "-p"],
            helper="Project name",
            value_type=str,
            default="demo",
            required=True,
        )

        flags = self.args._get_flag_objects()

        self.assertIs(flags["--project"], flags["-p"])
        self.assertEqual(flags["-p"].canonical_name, "--project")
        self.assertIn("--project", self.args.required_flags)

    def test_add_string_creates_string_flag(self):
        self.args.add_string(
            names=["-p"],
            helper="Project name",
            default="pyflag",
        )

        flags = self.args.get_flags()

        self.assertIn("-p", flags)
        self.assertEqual(flags["-p"], "pyflag")
        self.assertIsInstance(flags["-p"], str)

    def test_add_int_creates_int_flag(self):
        self.args.add_int(
            names=["-n"],
            helper="Number of retries",
            default=3,
        )

        flags = self.args.get_flags()

        self.assertIn("-n", flags)
        self.assertEqual(flags["-n"], 3)
        self.assertIsInstance(flags["-n"], int)
    
    def test_add_float_creates_float_flag(self):
        self.args.add_float(
            names=["-n"],
            helper="Number of retries",
            default=3.0,
        )

        flags = self.args.get_flags()

        self.assertIn("-n", flags)
        self.assertEqual(flags["-n"], 3.0)
        self.assertIsInstance(flags["-n"], float)

    def test_add_bool_creates_bool_flag(self):
        self.args.add_bool(
            names=["--verbose"],
            helper="Enable verbose output",
            default=True,
        )

        flags = self.args.get_flags()

        self.assertIn("--verbose", flags)
        self.assertEqual(flags["--verbose"], True)
        self.assertIsInstance(flags["--verbose"], bool)

    def test_add_file_creates_file_flag(self):
        self.args.add_file(
            names=["--config"],
            helper="Config file path",
            default="",
        )

        flag_objects = self.args._get_flag_objects()

        self.assertIn("--config", flag_objects)
        self.assertIs(flag_objects["--config"].value_type, Path)

    def test_check_flag_returns_true_for_existing_flag(self):
        self.args.add_string(
            names=["-p"],
            helper="Project name",
            default="pyflag",
        )

        self.assertTrue(self.args.check_flag("-p"))

    def test_check_flag_returns_false_for_missing_flag(self):
        self.args.add_string(
            names=["-p"],
            helper="Project name",
            default="pyflag",
        )

        self.assertFalse(self.args.check_flag("--project"))

    def test_helper_text_is_stored_for_each_flag(self):
        self.args.add_string(
            names=["-p", "--project"],
            helper="Project name",
            default="pyflag",
        )

        self.assertIn("Project name", self.args.helpers["-p"])
        self.assertIn("Type:", self.args.helpers["-p"])
        self.assertIn("str", self.args.helpers["-p"])

    def test_get_value_returns_flag_value(self):
        self.args.add_string(
            names=["--project"],
            helper="Project name",
            default="demo-app",
        )

        self.assertEqual(self.args.get_value("--project"), "demo-app")

    def test_was_provided_is_false_before_parse(self):
        self.args.add_string(
            names=["--project"],
            helper="Project name",
        )

        self.assertFalse(self.args.has_value("--project"))

    def test_get_optional_returns_default_when_not_set(self):
        self.args.add_string(
            names=["--output"],
            helper="Output file",
        )

        self.assertEqual(self.args.get_optional("--output", "./results.json"), "./results.json")



class TestParse(unittest.TestCase):
    def setUp(self):
        self.args = Flags()

    def test_parse_sets_alias_and_canonical_values_together(self):
        self.args.add_string(names=["--project", "-p"], helper="Project name")

        self.args.parse(["-p", "demo"])

        self.assertEqual(self.args.get_value("--project"), "demo")
        self.assertEqual(self.args.get_value("-p"), "demo")
        self.assertEqual(
            self.args.get_flags(),
            {"--project": "demo", "-p": "demo"},
        )

    def test_parse_sets_bool_flag_true_when_present(self):
        self.args.add_bool(names=["--verbose"], helper="Verbose mode", default=False)

        self.args.parse(["--verbose"])

        flags = self.args.get_flags()
        self.assertTrue(flags["--verbose"])

    def test_parse_sets_bool_flag_true_with_yes_equals_syntax(self):
        self.args.add_bool(names=["--verbose"], helper="Verbose mode", default=False)

        self.args.parse(["--verbose=yes"])

        self.assertTrue(self.args.get_value("--verbose"))

    def test_parse_sets_bool_flag_false_with_equals_syntax(self):
        self.args.add_bool(names=["--verbose"], helper="Verbose mode", default=True)

        self.args.parse(["--verbose=false"])

        self.assertFalse(self.args.get_value("--verbose"))

    def test_parse_sets_bool_flag_false_with_off_equals_syntax(self):
        self.args.add_bool(names=["--verbose"], helper="Verbose mode", default=True)

        self.args.parse(["--verbose=off"])

        self.assertFalse(self.args.get_value("--verbose"))

    def test_parse_rejects_split_bool_value(self):
        self.args.add_bool(names=["--verbose"], helper="Verbose mode", default=False)

        with self.assertRaises(ValueError):
            self.args.parse(["--verbose", "false"])

    def test_parse_rejects_invalid_bool_value_with_equals_syntax(self):
        self.args.add_bool(names=["--verbose"], helper="Verbose mode", default=False)

        with self.assertRaises(ValueError):
            self.args.parse(["--verbose=maybe"])

    def test_parse_sets_string_flag_value(self):
        self.args.add_string(names=["-p"], helper="Project name", default="")

        self.args.parse(["-p", "demo"])

        flags = self.args.get_flags()
        self.assertEqual(flags["-p"], "demo")
    
    def test_parse_sets_int_flag_value(self):
        self.args.add_int(names=["--number"], helper="A random number")

        self.args.parse(["--number", "1"])

        flags = self.args.get_flags()
        self.assertIsInstance(flags["--number"], int)
        self.assertEqual(flags["--number"], 1)

    def test_parse_sets_value_with_equals_syntax(self):
        self.args.add_string(names=["--env"], helper="Environment")

        self.args.parse(["--env=prod"])

        self.assertEqual(self.args.get_value("--env"), "prod")

    def test_parse_sets_int_value_with_equals_syntax(self):
        self.args.add_int(names=["--workers"], helper="Worker count")

        self.args.parse(["--workers=4"])

        self.assertEqual(self.args.get_value("--workers"), 4)

    def test_parse_rejects_invalid_int_value(self):
        self.args.add_int(names=["--workers"], helper="Worker count")

        with self.assertRaises(ValueError):
            self.args.parse(["--workers", "four"])

    def test_parse_rejects_invalid_float_value(self):
        self.args.add_float(names=["--ratio"], helper="Ratio")

        with self.assertRaises(ValueError):
            self.args.parse(["--ratio", "nope"])

    def test_parse_sets_float_flag_value(self):
        self.args.add_float(names=["--number"], helper="A random number")

        self.args.parse(["--number", "1.0"])

        flags = self.args.get_flags()
        self.assertIsInstance(flags["--number"], float)
        self.assertEqual(flags["--number"], 1.0)

    def test_parse_sets_file_flag_value_when_file_exists(self):
        self.args.add_file(names=["--config"], helper="Config file path", default="")

        with NamedTemporaryFile() as temp_file:
            self.args.parse(["--config", temp_file.name])

            flags = self.args.get_flags()
            self.assertEqual(flags["--config"], temp_file.name)

    def test_parse_file_flag_raises_when_file_is_missing(self):
        self.args.add_file(names=["--config"], helper="Config file path", default="")

        with self.assertRaises(FileNotFoundError):
            self.args.parse(["--config", "missing-config-file.txt"])

    def test_parse_runs_validator_for_valid_int_value(self):
        self.args.add_int(
            names=["--port"],
            helper="Server port",
            validator=lambda value: 1 <= value <= 65535,
        )

        self.args.parse(["--port", "8080"])

        self.assertEqual(self.args.get_value("--port"), 8080)

    def test_parse_raises_when_validator_rejects_value(self):
        self.args.add_int(
            names=["--port"],
            helper="Server port",
            validator=lambda value: 1 <= value <= 65535,
        )

        with self.assertRaises(ValueError):
            self.args.parse(["--port", "70000"])

    def test_parse_runs_validator_for_string_value(self):
        self.args.add_string(
            names=["--env"],
            helper="Environment name",
            validator=lambda value: value in ["dev", "test", "prod"],
        )

        self.args.parse(["--env", "prod"])

        self.assertEqual(self.args.get_value("--env"), "prod")

    def test_parse_accepts_valid_string_choice(self):
        self.args.add_string(
            names=["--env"],
            helper="Environment name",
            choices=["dev", "test", "prod"],
        )

        self.args.parse(["--env", "dev"])

        self.assertEqual(self.args.get_value("--env"), "dev")

    def test_parse_rejects_invalid_string_choice(self):
        self.args.add_string(
            names=["--env"],
            helper="Environment name",
            choices=["dev", "test", "prod"],
        )

        with self.assertRaises(ValueError):
            self.args.parse(["--env", "staging"])

    def test_parse_accepts_valid_int_choice(self):
        self.args.add_int(
            names=["--workers"],
            helper="Worker count",
            choices=[1, 2, 4],
        )

        self.args.parse(["--workers", "2"])

        self.assertEqual(self.args.get_value("--workers"), 2)
    
    def test_parse_accepts_valid_float_choice(self):
        self.args.add_float(
            names=["--workers"],
            helper="Worker count",
            choices=[1.0, 2.0, 4.0],
        )

        self.args.parse(["--workers", "2.0"])

        self.assertEqual(self.args.get_value("--workers"), 2.0)

    def test_parse_rejects_invalid_int_choice(self):
        self.args.add_int(
            names=["--workers"],
            helper="Worker count",
            choices=[1, 2, 4],
        )

        with self.assertRaises(ValueError):
            self.args.parse(["--workers", "3"])
    
    def test_parse_rejects_invalid_float_choice(self):
        self.args.add_float(
            names=["--workers"],
            helper="Worker count",
            choices=[1.0, 2.0, 4.0],
        )

        with self.assertRaises(ValueError):
            self.args.parse(["--workers", "3.0"])
    
    def test_parse_converts_custom_parser(self):
        def convert_float(x) -> Any:
            try: 
                return float(x) 
            except: 
                return False
            
        self.args.add(
            names=["--workers"],
            helper="Worker count",
            value_type=float,
            choices=[1.0, 2.0, 4.0],
            custom_parse=lambda x: convert_float(x),
        )

        self.args.parse(["--workers", "2.0"])

        self.assertEqual(self.args.get_value("--workers"), 2.0)

    @patch("builtins.input", return_value="my-app")
    def test_interactive_mode_prompts_for_missing_required_flag(self, mock_input):
        self.args.add_string(
            names=["--project", "-p"],
            helper="Project name",
            required=True,
        )
        self.args.activate_interactive_mode()

        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.args.parse([])
            self.args.resolve_all()

        self.assertEqual(self.args.get_value("--project"), "my-app")
        self.assertIn("--project (str) is required.", stdout.getvalue())
        self.assertIn("Project name", stdout.getvalue())
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="./results.json")
    def test_resolve_prompts_for_missing_optional_value(self, mock_input):
        self.args.add_string(
            names=["--output"],
            helper="Output file",
        )
        self.args.activate_interactive_mode()

        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            value = self.args.resolve("--output")

        self.assertEqual(value, "./results.json")
        self.assertTrue(self.args.has_value("--output"))
        self.assertIn("--output (str) is required.", stdout.getvalue())
        self.assertIn("Output file", stdout.getvalue())
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="demo-app")
    def test_parse_and_resolve_enables_interactive_mode_and_prompts(self, mock_input):
        self.args.add_string(
            names=["--project", "-p"],
            helper="Project name",
            required=True,
        )

        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.args.parse_and_resolve([])

        self.assertTrue(self.args.interactive_mode)
        self.assertEqual(self.args.get_value("--project"), "demo-app")
        self.assertIn("--project (str) is required.", stdout.getvalue())
        mock_input.assert_called_once()

    def test_resolve_all_raises_for_missing_required_flag(self):
        self.args.add_string(
            names=["--project", "-p"],
            helper="Project name",
            required=True,
        )

        with self.assertRaises(ValueError):
            self.args.resolve_all()

    def test_help_text_prints_registered_helpers(self):
        self.args.add_string(
            names=["--project", "-p"],
            helper="Project name",
            default="demo",
        )

        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.args.help_text()

        output = stdout.getvalue()
        self.assertIn("USAGE:", output)
        self.assertIn("flag='--project'", output)
        self.assertIn("flag='-p'", output)
        self.assertIn("Project name", output)
        self.assertIn("Default Value is set as: demo", output)

    def test_debug_flags_returns_json_string(self):
        self.args.add_string(
            names=["--project"],
            helper="Project name",
        )
        self.args.parse(["--project", "my-app"])

        result = self.args.debug_flags()

        self.assertEqual(json.loads(result), {"--project": "my-app"})
    
    def test_parse_missing_flag_value(self):

        with self.assertRaises(ValueError):
            self.args.parse(["--number", "1"])

    def test_parse_missing_required_value(self):
        self.args.add_int(names=["--number", "-n"], helper="A random number", required=True)

        with self.assertRaises(ValueError):
            self.args.parse(["1"])

if __name__ == "__main__":
    unittest.main()
