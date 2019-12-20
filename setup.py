from pydamage import __version__
from setuptools import setup, find_packages


setup(
    name='pydamage',
    version=__version__,
    description='Damage parameter estimation for ancient DNA',
    long_description=open("README.md").read(),
    url='https://github.com/maxibor/pydamage',
    long_description_content_type="text/markdown",
    license='GNU-GPLv3',
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pydamage = pydamage.cli:cli'
        ]
    }
)