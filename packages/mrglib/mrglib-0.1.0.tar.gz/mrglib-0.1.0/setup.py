from setuptools import find_packages, setup

setup(
    name='mrglib',
    packages=find_packages(include=['mrglib']),
    version='0.1.0',
    description='Library wrapping many mrg functionalities',
    author='Jelena Mirkovic, USC/ISI, mirkovic@isi.edu',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
