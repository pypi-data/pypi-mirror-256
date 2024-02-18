from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Stucent',
    version='0.1.3',  # Update this for every release
    packages=find_packages(),
    install_requires=requirements,
    # Add all other necessary package metadata
)
