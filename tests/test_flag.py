import unittest
from pyflags.flag import argument

class TestArgument(unittest.TestCase):
    def setUp(self):
        self.args = argument()

    def test_add_string_creates_string_flag(self):
        self.args.add_string(
            arguments=["-p"],
            helper="Project name",
            default="pyflag",
        )

        flags = self.args.get_flags()

        self.assertIn("-p", flags)
        self.assertEqual(flags["-p"].value, "pyflag")
        self.assertIs(flags["-p"].type, str)

    def test_add_int_creates_int_flag(self):
        self.args.add_int(
            arguments=["-n"],
            helper="Number of retries",
            default=3,
        )

        flags = self.args.get_flags()

        self.assertIn("-n", flags)
        self.assertEqual(flags["-n"].value, 3)
        self.assertIs(flags["-n"].type, int)

    def test_add_bool_creates_bool_flag(self):
        self.args.add_bool(
            arguments=["--verbose"],
            helper="Enable verbose output",
            default=True,
        )

        flags = self.args.get_flags()

        self.assertIn("--verbose", flags)
        self.assertEqual(flags["--verbose"].value, True)
        self.assertIs(flags["--verbose"].type, bool)

    def test_check_flag_returns_true_for_existing_flag(self):
        self.args.add_string(
            arguments=["-p"],
            helper="Project name",
            default="pyflag",
        )

        self.assertTrue(self.args.check_flag("-p"))

    def test_check_flag_returns_false_for_missing_flag(self):
        self.args.add_string(
            arguments=["-p"],
            helper="Project name",
            default="pyflag",
        )

        self.assertFalse(self.args.check_flag("--project"))

    def test_helper_text_is_stored_for_each_flag(self):
        self.args.add_string(
            arguments=["-p", "--project"],
            helper="Project name",
            default="pyflag",
        )

        self.assertEqual(self.args.helpers["-p"], "Project name")
        self.assertEqual(self.args.helpers["--project"], "Project name")


class TestParse(unittest.TestCase):
    def test_parse_sets_bool_flag_true_when_present(self):
        args = argument()
        args.add_bool(arguments=["--verbose"], helper="Verbose mode", default=False)

        args.parse(["--verbose"])

        flags = args.get_flags()
        self.assertTrue(flags["--verbose"].value)

    def test_parse_sets_string_flag_value(self):
        args = argument()
        args.add_string(arguments=["-p"], helper="Project name", default="")

        args.parse(["-p", "demo"])

        flags = args.get_flags()
        self.assertEqual(flags["-p"].value, "demo")

if __name__ == "__main__":
    unittest.main()
