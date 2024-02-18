from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()
setup(
    name='gridcreator',
    version='0.1.2',
    author='oblivisheee',
    author_email='molniya213y@gmail.com',
    description='That library provides utilities to create grids.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    license='GNU General Public License Version 3',
    url='https://github.com/endprivate/grid'
)
