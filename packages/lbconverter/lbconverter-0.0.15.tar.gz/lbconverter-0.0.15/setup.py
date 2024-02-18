from setuptools import setup, find_packages

with open("src/readme.md") as f:
    long_description = f.read()

setup(
name='lbconverter',
version='0.0.15',
author='Gabe',
author_email='gunderwood@labelbox.com',
long_description=long_description,
long_description_content_type= "text/markdown",
description='module of classes to assist on getting model results to labelbox',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)