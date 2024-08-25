# Notubiz

## Requirements 
Python >= 3.9

`py -m venv .venv`
`pip install pip-compile-multi`

## Installation
First run
`pip-compile '.\requirements.in'`
to generate `requirements.txt`.

Then run `.\.venv\Scripts\Activate.ps1`
In venv run `py -m pip install -r .\requirements.txt`

`python setup.py install --user`