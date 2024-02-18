# setup.py

from setuptools import setup

setup(
    name='dynodb',
    version='0.3.0',
    packages=[''],
    install_requires=['requests','argparse'],
    entry_points={
        'console_scripts': [
            'dynodb = dynodb:main',
        ],
    },
)
