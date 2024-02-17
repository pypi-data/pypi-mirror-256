from setuptools import find_packages, setup

# Read the requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='visionVault',
    packages=find_packages(include=['visionVault']),
    version='0.1.0',
    description='Image profiling library',
    author='@itertools',
    install_requires='requirements.txt',  # Include requirements from requirements.txt
)
