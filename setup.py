import os
from setuptools import setup
from aclinks import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

settings = dict(
    name = 'awesome-check-link',
    packages = ['aclinks'],
    version = __version__,
    author = 'shadawck',
    author_email = 'hug211mire@gmail.com',
    description = ('Check if links in md file and more particuraly in awesome-list are down or not.'),
    license = 'MIT',
    keywords = 'awesome-check-link, awesome, awesome list, checker, down, link checker',
    url = 'https://github.com/remiflavien1/awesome-check-link',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        "console_scripts": [
            "aclinks=aclinks.__main__:main",
        ]
    },
)

setup(**settings)

