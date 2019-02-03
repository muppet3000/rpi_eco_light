import os
import re

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

del os.link


def parse_version(package_name):
    """
    if environment variable PACKAGE_VERSION set use that as version number
    else open `version_file` and find `__version__ = x.y.z`.
    thanks to http://stackoverflow.com/a/7071358
    """
    version = os.environ.get('PACKAGE_VERSION', None)
    if version:
        return version

    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_file = '{}/__init__.py'.format(package_name)
    with open(version_file, 'r') as f:
        file_contents = f.read()
    match = re.search(version_re, file_contents, re.M)
    if match:
        return match.group(1)
    else:
        raise RuntimeError('Unable to find version string in {}.'.format(version_file))


requirements_fn = os.path.join(os.path.dirname(__file__), 'requirements.txt')

setup(
    name='rpi-eco-light',
    version=parse_version('rpi_eco_light'),
    packages=find_packages(),
    include_package_data=True,
    author='Chris Straffon',
    author_email='muppet_3000@hotmail.com',
    url='https://github.com/muppet3000/rpi-eco-light',
    install_requires=[str(req) for req in parse_requirements(open(requirements_fn).read())],
    entry_points="""
    [console_scripts]
        rpi-eco-light = rpi_eco_light.eco_light:main
    """
)
