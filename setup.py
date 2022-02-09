# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='unifyname',
    version='0.1.0',
    description='unifyname package for Python-Guide.org',
    long_description=readme,
    author='Vincent Belz',
    author_email='vincent.belz@loft.com.br',
    url='https://github.com/vincent-belz/unifyname',
    license=license,
    packages=find_packages(exclude=('tests', 'data','demo'))
)
