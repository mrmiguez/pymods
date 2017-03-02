from setuptools import setup, find_packages

setup(
    name="pymods",
    version="0.0.4",
    packages=find_packages(),
    install_requires=['lxml >= 2.3'],
    author="Matthew Miguez",
    author_email="r.m.miguez@gmail.com",
    description=(
        "Utility class wrapping lxml for serializing data from MODS v3.4 XML metadata."
    ),
    keywords="MODS metadata xml",
)