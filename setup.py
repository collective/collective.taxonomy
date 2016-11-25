import os
import sys

reload(sys).setdefaultencoding("UTF-8")

from setuptools import setup, find_packages


def read(*pathnames):
    fh = open(os.path.join(os.path.dirname(__file__), *pathnames))
    return fh.read().decode('utf-8')

version = '1.4.3.dev0'

setup(
    name='collective.taxonomy',
    version=version,
    description="Create, edit and use hierarchical taxonomies in Plone!",
    long_description='\n'.join([
        read('README.rst'),
        read('CHANGES.rst'),
    ]),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
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
    install_requires=[
        'setuptools',
        'plone.supermodel',
        'plone.api',
        'plone.app.registry',
        'plone.app.dexterity',
    ],
    extras_require={
        'test': [
            'plone.testing',
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
