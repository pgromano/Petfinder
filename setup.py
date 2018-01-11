from setuptools import setup, Extension, find_packages

setup(
    name = 'petfinder',
    author = 'Pablo Romano',
    author_email = 'pablo.romano42@gmail.com',
    description = 'Python Interface to the Petfinder API ',
    version = '0.1',
    url = 'https://github.com/pgromano/petfinder',

    packages = ['petfinder'],
    install_requires=[
        'requests',
        'lxml'
    ],
    zip_safe = False,
)
