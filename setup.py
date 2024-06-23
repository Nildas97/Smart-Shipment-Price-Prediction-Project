# importing libraries
from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = "-e ."


# defining function to fetch the requirements.txt
# takes input a filepath as string
# gives output a list of strings


def get_requirements(filepath: str) -> List[str]:
    # create an empty list
    requirements = []

    # opening the filepath as file_object
    with open(filepath) as file_obj:
        # read the lines through requirements.txt
        requirements = file_obj.readlines()

        # in requirements.txt file every line has new line operator.
        # removing the new line operator to readlines the through it.
        requirements = [i.replace("\n", "") for i in requirements]

        # removing the (-e .) from requirements.txt
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)


setup(name='ML_Application_Project',
      version='0.0.1',
      description='Machine Learning Application Project',
      author='Nilutpal Das',
      author_email='nilutpaldas992@gmail.com',
      packages=find_packages(),
      install_requires=get_requirements("requirements.txt")
      )
