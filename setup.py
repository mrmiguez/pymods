from setuptools import setup, find_packages

setup(
    name="pymods",
    version="0.0.5",
    packages=find_packages(exclude=['tests*']),
    install_requires=['lxml >= 2.3'],
    author="Matthew Miguez",
    author_email="r.m.miguez@gmail.com",
    description=(
        "Utility class wrapping lxml for serializing data from MODS v3.4 XML metadata."
    ),
    url='https://github.com/mrmiguez/pymods',
    keywords="MODS metadata xml",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)