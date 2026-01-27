
from setuptools import setup, find_packages
with open('requirements.txt', encoding = 'utf-8') as f:
    requirements = f.read().splitlines()
setup(
    name='playground-series-s5e12',
    version='0.1.0',
    author = 'Krishna',
    packages=find_packages(),
    install_requires=requirements,
)
