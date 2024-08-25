import os
from setuptools import setup 

NAME = "notubiz"
VERSION = "0.0.1"

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    LONG_DESCRIPTION = readme.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name=NAME,
    version=VERSION,
    description="Notubiz",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    author="Rutger Rauws",
    url="https://github.com/RutgerRauws/python-notubiz",
    keywords=["notubiz", "Notubiz"],
    install_requires=requirements,
    include_package_data=True
)