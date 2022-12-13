import os

from setuptools import find_packages
from setuptools import setup

version = '3.0.0'


def read(*pathnames):
    with open(os.path.join(os.path.dirname(__file__), *pathnames)) as fh:
        return fh.read()


setup(
    name='collective.taxonomy',
    version=version,
    description="Create, edit and use hierarchical taxonomies in Plone!",
    url='https://pypi.org/project/collective.taxonomy/',
    long_description='\n'.join([
        read('README.rst'),
        read('CHANGES.rst'),
    ]),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords='plone taxonomy dexterity',
    author='Bo Simonsen and Malthe Borch',
    author_email='bo@headnet.dk',
    license="GPLv2+",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        'setuptools',
        'plone.supermodel',
        'plone.api >= 1.5',
        'plone.app.registry',
        'lxml',
        'six >= 1.12',
    ],
    extras_require={
        'dev': [
            'zest.releaser[recommended]',
        ],
        'test': [
            'plone.testing',
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.querystring',
            'plone.app.robotframework[debug]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
