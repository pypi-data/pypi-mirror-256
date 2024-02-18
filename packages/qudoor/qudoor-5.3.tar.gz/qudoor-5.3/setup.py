from setuptools import setup, find_packages

# Lire le contenu du README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qudoor',
    version='5.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
    ],
    # Utilisez le contenu du README comme description longue
    long_description=long_description,
    long_description_content_type='text/markdown',  # Indiquez que c'est du markdown
)
