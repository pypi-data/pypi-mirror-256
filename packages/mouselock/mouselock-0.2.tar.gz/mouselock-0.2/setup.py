from setuptools import setup, find_packages

setup(
    name="mouselock",
    description="A Python package for easily and programmatically locking your mouse.",
    long_description=open("long-description.txt").read(),
    version="0.2",
    packages=find_packages()
)