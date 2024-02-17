from setuptools import setup, find_packages

setup(
    name="gmt-gerby",
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
