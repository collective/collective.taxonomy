from setuptools import setup
setup(
    # thanks to this bug
    # https://github.com/pypa/setuptools/issues/1136
    # we need one line in here:
    # fixed in https://setuptools.readthedocs.io/en/latest/history.html#v40-7-0
    # but plone 5.1 used older.
    package_dir={"": "src"}
)