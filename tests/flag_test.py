import unittest
import pyflags

new_arg = pyflags.argument()
new_arg.add_string(arguments=["-p"], helper="The name of the project and virtual enviornment")
new_arg.add_string(arguments=["-t"], helper="The type of project - currently supportedi golang and python")

print(new_arg.helper())
print(new_arg.check_flag("--p"))
print(new_arg.check_flag("-p"))