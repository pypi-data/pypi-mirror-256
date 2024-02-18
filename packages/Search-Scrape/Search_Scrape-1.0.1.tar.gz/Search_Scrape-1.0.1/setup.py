from setuptools import setup, find_packages

setup(
    name='Search_Scrape',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
      'requests',
      'beautifulsoup4',
    ],
)
