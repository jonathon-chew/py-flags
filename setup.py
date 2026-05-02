from setuptools import find_packages
from setuptools import setup

setup (
    name="pyflags",
    version="v0.6.3",
    description="`py-flags` is a small Python project for defining and parsing command-line flags.",
    author="Jonathon Chew",
    author_email="jonchew626@hotmail.com",
    url="https://github.com/jonathon-chew/py-flags",
    packages=find_packages(where="src", exclude=("tests*",)),
)
