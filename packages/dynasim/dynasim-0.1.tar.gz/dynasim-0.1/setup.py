from setuptools import setup

VERSION = '0.1'
DESCRIPTION = 'Dynamic System Simulators'
LONG_DESCRIPTION = 'Something long'

setup(
    name='dynasim',
    version=VERSION,
    author='Marcus Haywood-Alexander',
    author_email='<mhaywood@ethz.ch>',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # license='MIT',
    packages=['dynasim'],
    package_dir={'':'src'},
    include_package_data=False,
    install_requires=[
        'numpy'
        ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)