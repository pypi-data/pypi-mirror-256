from setuptools import setup, find_packages

setup(
    name="py-dimg4md", 
    version="0.1.2", 
    packages=find_packages(),
    readme="README.md",
    entry_points={
        'console_scripts': [
            'dimg = dimg4md.cli:cli',
        ]
    })