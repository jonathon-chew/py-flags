# CHANGELOG

	## v0.7.0 

		### UPDATES
		1. remove build folder from repo
		### DELETES
		1. build folder and contents as remmance
		### MISC
		1. where it looks for packages
		1. where it looks for packages

	## v0.6.3 

		### NEW
		1. setup.py for installation purposes
		1. __init__ imports to be able to import better into other projects
		1. removing some empty values from get_flags; update: readme to match new behaviour and decisions
		### UPDATES
		1. show how to pip install from github
		### REFACTORS
		1. move everything into a src directory

	## v0.6.2 

		### UPDATES
		1. remove empty list from get_keys, useful when debugging
		1. README includes 2 new features class.flag to get the value and now support lists

	## v0.6.1 

		### NEW
		1. ability to add lists of values

	## v0.6.0 

		### NEW
		1. test for new feat around class.name functionality
		### UPDATES
		1. change str|int|float|bool to Any to fix Pydantic errors / warnings

	## v0.5.2 

		### NEW
		1. support for accessing flags by simple calling class initation and . flag name

	## v0.5.1 

		### NEW
		1. function to display help text - required flags then non-required, parse and resolve function so users don't have to call both in 2 seperate functions, also sets interative mode to be on! parse now allows for booleans to be false under certain circumstances; update: test suite for more functionality and more edge cases, as well as adjusting for the new functionality;

	## v0.5.0 

		### UPDATES
		1. changing license
		### REFACTORS
		1. logic to use inline python code as opposed to more explicit loops; update: .gitignore for local files and reference; delete: requirements as trying for a no dependency build
		### MISC
		1. Add MIT License to the project

	## v0.4.2 

		### NEW
		1. interactive prompting, custom parsing, float + equals-style parsing; update: tests and README to highlight guided CLI USP

	## v0.4.1 

		### NEW
		1. highlighting the new interactive feat. if missing required flags and how this project is different
		1. tests for all the new feats from commit b33d16f
		1. return flags as json, interactive mode for users to add required flags if missed, custom parsing added as an option to convert; refactor: parsing logic to it's own function

	## v0.4.0 

		### NEW
		1. add the ability for choices!
		### UPDATES
		1. docs

	## v0.3.0 

		### UPDATES
		1. pythonic updates
		1. cleaning up

	## v0.2.1 

		### NEW
		1. add_file function which checks file existance based on what the user put it, allows for a function to be passed in by the user to confirm the input of the user is correct; update: get_flags only returns only flags with values not all possible flags

	## v0.2.0 

		### UPDATES
		1. general clean up

	## v0.1.3 

		### NEW
		1. generic add API and shared alias handling; update: README examples and test coverage

	## v0.1.2 

		### NEW
		1. shared alias/canonical flag handling; update: README with alias-based usage examples

	## v0.1.1 

		### NEW
		1. adding get_value for a cleaner nicer user API
		### UPDATES
		1. Update the README to reflect more about what the project is - not just what it will be and it's aims/goals

	## v0.1.0 

		### NEW
		1. adding useage examples