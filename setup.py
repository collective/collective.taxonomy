import os
import sys

reload(sys).setdefaultencoding("UTF-8")

from setuptools import setup, find_packages


def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read().\
           decode('utf-8')

version = '0.1'

setup(name='collective.taxonomy',
      version=version,
      description="Add-on for Plone to handle taxonomies for z3cform content.",
      long_description='\n'.join([
          read('README.rst'),
          read('CHANGES.rst'),
          ]),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='plone taxonomy dexterity',
      author='Bo Simonsen',
      author_email='bo@headnet.dk',
      license="GPLv2+",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,

      # If the dependency to z3c.form gives you trouble within a Zope
      # 2 environment, try the `fakezope2eggs` recipe
      install_requires=[
          'setuptools',
          'plone.app.registry',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
