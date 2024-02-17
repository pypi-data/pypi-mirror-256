from setuptools import setup, find_packages

setup(
    name="gmt-gerby",
    description="flask-based web application for managing a gerby-plastex site",
    version="0.1.1",
    author="Pieter Belmans",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "PyPDF2",
        "Markdown",
        "python-markdown-math",
        "validators",
        "peewee",
        "flask_profiler",
        # "mdx_bleach ",
        # "pybtex",
        "feedparser",
        "networkx"])
