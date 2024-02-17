from setuptools import setup, find_packages

setup(
    name='qudoor',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        # Listez vos dépendances ici
        'numpy',
        'matplotlib',
        'scipy'
        # ...
    ],
)

