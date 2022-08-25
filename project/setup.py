"""This is only used to add the directory to your PYTHONPATH in a non-hacky way

Actual packaging should be done with the package commands in the project.yml file.
"""

from setuptools import setup, find_packages

setup(name="stp-editable", packages=find_packages())
