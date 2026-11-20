from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pymods",
    version="2.0.15",
    packages=find_packages(exclude=['tests*']),
    install_requires=['lxml >= 2.3'],
    author="Matthew Miguez",
    author_email="r.m.miguez@gmail.com",
    description="Utility class wrapping lxml for reading data from MODS XML metadata into Python data types.",
    long_description=long_description,
    url='https://github.com/mrmiguez/pymods',
    download_url='https://github.com/mrmiguez/pymods/archive/2.0.15.tar.gz',
    keywords="MODS metadata xml",
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)
