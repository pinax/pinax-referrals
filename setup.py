PACKAGE = "anafero"
NAME = "anafero"
DESCRIPTION = "a referrals app for Django"
AUTHOR = "Eldarion"
AUTHOR_EMAIL = "paltman@eldarion.com"
URL = "http://github.com/eldarion/anafero"
VERSION = __import__(PACKAGE).__version__

import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    url=URL,
    license="BSD",
    packages=find_packages(),
    install_requires=[
        "django-appconf==0.5"
    ],
    tests_require=[
        "Django>=1.4",
    ],
    test_suite="runtests.runtests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
