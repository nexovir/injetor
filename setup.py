from setuptools import setup, find_packages

setup(
    name='injector',
    version='1.0.0',
    description='Smart parameter injection tool',
    author='nexovir',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'injector=injector.cli:main',
        ],
    },
    install_requires=[
        'colorama',
        'requests',
        'pyfiglet',
    ],
    python_requires='>=3.6',
)
