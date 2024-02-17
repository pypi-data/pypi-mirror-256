from setuptools import setup

VERSION = '0.0.0'
DESCRIPTION = 'Airbnb scraper in Python'
LONG_DESCRIPTION = "This project is an open-source tool developed in Python for extracting product information from Airbnb. It's designed to be fast, and easy to use, making it an ideal solution for developers looking for Airbnb product data."

setup(
    name="gobnb",
    version=VERSION,
    author="John (John Balvin)",
    author_email="<johnchristian@hotmail.es>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    keywords=['airbnb', 'scraper', 'crawler'],
    install_requires=['curl_cffi','bs4'],
)