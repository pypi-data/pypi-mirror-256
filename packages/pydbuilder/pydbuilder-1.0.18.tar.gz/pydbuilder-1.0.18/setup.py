from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pydbuilder',
    version='1.0.18',
    description='Utility for creating pyd files using Cython',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Cherepok3',
    packages=['pydbuilder'],
    package_data={
        'pydbuilder': ['language.json', 'settings.json'],
    },
    install_requires=[
        'setuptools',
        'cython'
    ],
    entry_points={
        'console_scripts': [
            'pydbuilder=pydbuilder.pydbuilder:main',
        ],
    }
)