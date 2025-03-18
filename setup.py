from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "3.1.6"
long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)


setup(
    name="collective.taxonomy",
    version=version,
    description="Create, edit and use hierarchical taxonomies in Plone!",
    url="https://pypi.org/project/collective.taxonomy/",
    long_description=long_description,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: Addon",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="plone taxonomy dexterity",
    author="Bo Simonsen and Malthe Borch",
    author_email="bo@headnet.dk",
    license="GPLv2+",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "setuptools",
        "plone.base",
        "plone.supermodel",
        "plone.api >= 1.5",
        "plone.app.registry",
        "plone.app.dexterity",
        "lxml",
    ],
    extras_require={
        "dev": [
            "zest.releaser[recommended]",
        ],
        "test": [
            "mock",
            "plone.api",
            "plone.app.caching",
            "plone.app.contenttypes",
            "plone.app.contenttypes[test]",
            "plone.app.iterate",
            "plone.app.querystring",
            "plone.app.robotframework[debug]",
            "plone.app.testing",
            "plone.restapi[test]",
            "plone.testing",
            "requests",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
