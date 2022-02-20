## Venv Instructions

Navigate to root folder

Set up folder
`python -m venv env`
Activate new environment
`.\env\Scripts\activate`
Install some packages
`python -m pip install pandas pip-chill`
Record those installations
`pip-chill > requirements.txt`

## Put on another machine
Build new folder
`python -m venv env`
activate new environment
`.\env\Scripts\activate`
Download the required packages from list
`python -m pip install -r requirements.txt`
