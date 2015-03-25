import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


NAME = "pinax-referrals"
DESCRIPTION = "a referrals app for Django"
AUTHOR = "Pinax Team"
AUTHOR_EMAIL = "developers@pinaxproject.com"
URL = "http://github.com/pinax/pinax-referrals"
VERSION = "2.1.0"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    url=URL,
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "django-appconf==1.0.1"
    ],
    package_data={
        "pinax.referrals": [
            "templates/pinax/referrals/*",
        ]
    },
    tests_require=[
        "Django>=1.5",
    ],
    test_suite="runtests.runtests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
