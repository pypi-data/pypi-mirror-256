from setuptools import setup, find_packages

with open("lbconverter/README.md", "r") as f:
    long_description = f.read()

setup(
name='lbconverter',
version='0.0.13',
author='Gabe',
author_email='gunderwood@labelbox.com',
long_description=long_description,
long_description_content_type = "text/markdown",
description='Module of classes to assist on getting model results to labelbox',
packages=find_packages(),
url="https://github.com/Gabefire/labelbox_converter",
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
install_requires=["labelbox[data]", "ultralytics"]
)