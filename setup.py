"""Install script for mpischedule
"""
__version__ = 0.1
__author__ = "Christopher Körber"

import os
from setuptools import setup


THIS_DIR = os.path.dirname(os.path.realpath(__file__))

REQ_FILE = os.path.join(THIS_DIR, "requirements.txt")
with open(REQ_FILE, "r") as f:
    REQUIREMENTS = f.read()
REQUIREMENTS = [el.strip() for el in REQUIREMENTS.split(",")]

README = os.path.join(THIS_DIR, "Readme.txt")
with open(REQ_FILE, "r", encoding="utf-8") as f:
    LONG_DESC = f.read()

setup(
    name="mpischedule",
    version=str(__version__),
    description="Package for scheduling parallel tasks",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author=__author__,
    license="MIT",
    packages=["mpischedule"],
    test_suite="tests",
    install_requires=REQUIREMENTS,
    url="https://github.com/ckoerber/mpi-schedule",
    keywords="mpi task scheduling",
)
