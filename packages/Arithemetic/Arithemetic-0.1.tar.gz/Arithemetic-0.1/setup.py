from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'This is sample package'
LONG_DESCRIPTION = 'A package to perform arithmetic operation'

# Setting up
setup(
    name="Arithemetic",
    version=VERSION,
    author="madhuri",
    author_email="madhurichowhan.official@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)