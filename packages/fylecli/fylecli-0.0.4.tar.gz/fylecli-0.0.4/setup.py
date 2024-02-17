import os

from setuptools import setup

setup(
    name='fylecli',
    version='0.0.4',
    description='File transfer',
    packages=['fyle_internals'],
    scripts=['fylecli.py'],
    entry_points={
        'console_scripts': [
            'fylecli = fylecli.fylecli:main'
        ]
    },
    include_package_data=True,
    platforms=['any'],
    author='Mark Smirnov',
    author_email='mark@mark99.ru'
)

os.chmod('fylecli.py', 0o755)
