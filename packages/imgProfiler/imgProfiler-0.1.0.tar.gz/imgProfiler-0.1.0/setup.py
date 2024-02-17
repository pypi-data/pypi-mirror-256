from setuptools import find_packages, setup

# Read the requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='imgProfiler',
    packages=find_packages(include=['imgProfiler']),
    version='0.1.0',
    description='Image profiling library',
    author='@itertools',
 # Include requirements from requirements.txt
)
