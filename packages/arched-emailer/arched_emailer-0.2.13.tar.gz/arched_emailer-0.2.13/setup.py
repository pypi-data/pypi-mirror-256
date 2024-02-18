from setuptools import setup

import arched_emailer

# Reading long description from README
with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

# Reading requirements from requirements.txt
with open("requirements.txt", "r", encoding='UTF-8') as fh:
    requirements = fh.read().splitlines()

setup(
    name='arched_emailer',
    version=arched_emailer.arched_emailer.__version__,
    packages=['arched_emailer'],
    description="A emailing python library",
    url='https://github.com/lewis-morris/arched_emailer',
    license='MIT',
    author='lewis',
    install_requires=requirements,
    author_email='lewis@arched.dev',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
