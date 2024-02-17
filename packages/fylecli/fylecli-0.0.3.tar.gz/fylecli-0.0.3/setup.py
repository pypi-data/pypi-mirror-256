import os

from setuptools import setup

setup(
    name='fylecli',
    version='0.0.3',
    description='File transfer',
    packages=['fyle_internals'],
    scripts=['fylecli.py'],
    entry_points={
        'console_scripts': [
            'fylecli=fylecli.fylecli:main'
        ]
    },
    include_package_data=True,
    platforms=['any'],
    author='Mark Smirnov',
    author_email='mark@mark99.ru'
)

open('fylecli', 'wb').write(open('fylecli.py', 'rb').read())
os.chmod('fylecli', 0o755)
