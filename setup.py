# previous problem: Import Error, about relative import

# Solution: using the setuptools. The consequence here is that the .venv must be in the highest root of the project 

from setuptools import setup, find_packages

setup(name="myproject", version="1.0", packages=find_packages())

# when initializing (like after you cloning from github, run these including setting up the .venv)
"""
python3 -m venv .venv # .venv is the name of the folder!

source .venv/bin/activate # activate the environment!

which python # check if the python comes from the .venv/bin folder!

# install any dependencies
pip install -e . # set package/* to an absolute position, which later can be access from any python file under this project root
pip install -r requirements.txt # if the requirements.txt is exist and you want to install all the packages inside

# set all dependencies to the requirements.txt file (if you are setting up for the first time)
pip freeze > requirements.txt

deactivate # deactivate the environment
"""

# Virtual Environment: venv

# Why? Because the program only runs in the same Raspi. We are not planned to move the program to another OS. So I think that it's better to use just venv and isolating the project dependencies.

# venv guidelines: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/