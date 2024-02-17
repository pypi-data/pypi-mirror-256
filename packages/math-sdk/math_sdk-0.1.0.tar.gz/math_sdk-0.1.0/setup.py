# setup.py
from setuptools import setup, find_packages

setup(
    name='math_sdk',
    version='0.1.0',
    author='Siva',
    author_email='sivaram2k10@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    description='An example SDK for basic math operations.',
    long_description=open('README.md').read(),
    install_requires=[
        # Any dependencies, in this case, there shouldn't be any
    ],
)