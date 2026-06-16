from pathlib import Path
from setuptools import setup

version = "3.1.8.dev0"
long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)


setup(
    name="collective.taxonomy",
    version=version,
    description="Create, edit and use hierarchical taxonomies in Plone!",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.taxonomy",
        "Source": "https://github.com/collective/collective.taxonomy",
        "Tracker": "https://github.com/collective/collective.taxonomy/issues",
    },
    long_description=long_description,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords="plone taxonomy dexterity",
    author="Bo Simonsen and Malthe Borch",
    author_email="bo@headnet.dk",
    license="GPLv2+",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "collective.collectionfilter",
        "lxml",
        "plone.api",
        "plone.app.contentmenu",
        "plone.app.contenttypes",
        "plone.app.multilingual",
        "plone.app.registry",
        "plone.app.vocabularies",
        "plone.app.z3cform",
        "plone.autoform",
        "plone.base",
        "plone.behavior",
        "plone.dexterity",
        "plone.i18n",
        "plone.indexer",
        "plone.memoize",
        "plone.namedfile",
        "plone.protect",
        "plone.restapi",
        "plone.supermodel",
        "z3c.form",
        "Products.CMFCore",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.robotframework[debug]",
            "plone.app.dexterity",
            "plone.app.querystring",
            "plone.app.testing",
            "plone.browserlayer",
            "plone.restapi[test]",
            "plone.schemaeditor",
            "plone.testing",
            "robotsuite",
            "zest.releaser[recommended]",
            "zest.pocompile",
            "zestreleaser.towncrier",
            "zest.releaser",
        ],
    },
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    """,
)
