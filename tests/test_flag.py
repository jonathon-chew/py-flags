import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile
from pyflags.flag import Flags

class TestArgument(unittest.TestCase):
    def setUp(self):
        self.args = Flags()

    def test_add_creates_string_flag(self):
        self.args.add(
            names=["-p"],
            helper="Project name",
            type=str,
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
            type=str,
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
        self.assertIs(flag_objects["--config"].type, Path)

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



class TestParse(unittest.TestCase):
    def test_parse_sets_bool_flag_true_when_present(self):
        args = Flags()
        args.add_bool(names=["--verbose"], helper="Verbose mode", default=False)

        args.parse(["--verbose"])

        flags = args.get_flags()
        self.assertTrue(flags["--verbose"])

    def test_parse_sets_string_flag_value(self):
        args = Flags()
        args.add_string(names=["-p"], helper="Project name", default="")

        args.parse(["-p", "demo"])

        flags = args.get_flags()
        self.assertEqual(flags["-p"], "demo")
    
    def test_parse_sets_int_flag_value(self):
        args = Flags()
        args.add_int(names=["--number"], helper="A random number", default="")

        args.parse(["--number", "1"])

        flags = args.get_flags()
        self.assertIsInstance(flags["--number"], int)
        self.assertEqual(flags["--number"], 1)

    def test_parse_sets_file_flag_value_when_file_exists(self):
        args = Flags()
        args.add_file(names=["--config"], helper="Config file path", default="")

        with NamedTemporaryFile() as temp_file:
            args.parse(["--config", temp_file.name])

            flags = args.get_flags()
            self.assertEqual(flags["--config"], temp_file.name)

    def test_parse_file_flag_raises_when_file_is_missing(self):
        args = Flags()
        args.add_file(names=["--config"], helper="Config file path", default="")

        with self.assertRaises(FileNotFoundError):
            args.parse(["--config", "missing-config-file.txt"])

    def test_parse_runs_validator_for_valid_int_value(self):
        args = Flags()
        args.add_int(
            names=["--port"],
            helper="Server port",
            validator=lambda value: 1 <= value <= 65535,
        )

        args.parse(["--port", "8080"])

        self.assertEqual(args.get_value("--port"), 8080)

    def test_parse_raises_when_validator_rejects_value(self):
        args = Flags()
        args.add_int(
            names=["--port"],
            helper="Server port",
            validator=lambda value: 1 <= value <= 65535,
        )

        with self.assertRaises(ValueError):
            args.parse(["--port", "70000"])

    def test_parse_runs_validator_for_string_value(self):
        args = Flags()
        args.add_string(
            names=["--env"],
            helper="Environment name",
            validator=lambda value: value in ["dev", "test", "prod"],
        )

        args.parse(["--env", "prod"])

        self.assertEqual(args.get_value("--env"), "prod")
    
    def test_parse_missing_flag_value(self):
        args = Flags()

        with self.assertRaises(ValueError):
            args.parse(["--number", "1"])

    def test_parse_missing_required_value(self):
        args = Flags()
        args.add_int(names=["--number", "-n"], helper="A random number", default="", required=True)

        with self.assertRaises(ValueError):
            args.parse(["1"])

if __name__ == "__main__":
    unittest.main()
