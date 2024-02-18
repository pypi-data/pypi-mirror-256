# coding: utf-8

"""
    Structify

    Structify's goal is to take every source of knowledge and represent it on one place, deduplicated in the format that you specify.

    Version: 0.1.0

    Contact: team@structify.ai
"""


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "structifyai"
VERSION = "0.0.1"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 1.10.5, < 2",
    "aenum"
]

setup(
    name=NAME,
    version=VERSION,
    description="Structify",
    author="Structify Team",
    author_email="team@structify.ai",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Structify"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Discuss directly with founders for license.",
    long_description_content_type='text/markdown',
    long_description="""\
    Structify&#39;s goal is to take every source of knowledge and represent it on one place, deduplicated in the format that you specify.
    """,  # noqa: E501
    package_data={"structifyai": ["py.typed"]},
)
