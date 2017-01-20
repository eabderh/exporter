
from setuptools import setup, find_packages

def fromfile(path):
    with open(path) as f:
        return f.read()

setup(
    # basic
    name='export',
    version='0.1.0',
    description='Export variables, dictionaries, modules, etc, to other modules/runtimes',
    long_description=fromfile('README.md'),
    # author
    author='Elias Abderhalden',
    author_email='elias@bytekite.io',
    # dist
    license=fromfile('LICENSE.txt'),
    #url=''
    # module
    packages=find_packages(exclude=('tests'))
)

