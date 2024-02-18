from setuptools import setup, find_packages

setup(
    name='checkov_custom_policies',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'checkov',
    ],
)