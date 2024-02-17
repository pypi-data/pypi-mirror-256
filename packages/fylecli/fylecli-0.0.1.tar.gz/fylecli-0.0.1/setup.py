from setuptools import setup

setup(
    name='fylecli',
    version='0.0.1',
    description='File transfer',
    packages=['fyle_internals'],
    scripts=['fylecli.py'],
    include_package_data=True,
    platforms=['any'],
    author='Mark Smirnov',
    author_email='mark@mark99.ru'
)
