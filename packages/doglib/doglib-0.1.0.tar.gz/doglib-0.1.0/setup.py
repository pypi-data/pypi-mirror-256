from setuptools import setup, find_packages
setup(
name='doglib',
version='0.1.0',
author='Anton Pollak',
author_email='anton.pollak@starcode.de',
description='A simple package to manage dogs. Its aim is to demonstrate the use of packages in Python.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)