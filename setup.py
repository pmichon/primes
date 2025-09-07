#!/usr/bin/env python3
"""
Setup script for Ulam Spiral Generator
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ulam-spiral-generator",
    version="4.3.0",
    author="Piotr Michon",
    description="Kompleksowy generator spirali Ulama z wizualizacją liczb pierwszych",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmichon/primes",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ulam-spiral=ulam_spiral:main',
            'ulam-grafika=generuj_grafike_spirali:main',
            'prime-cache=generuj_cache_pierwszych:main',
        ],
    },
    keywords="ulam spiral prime numbers mathematics visualization svg png",
    project_urls={
        "Bug Reports": "https://github.com/pmichon/primes/issues",
        "Source": "https://github.com/pmichon/primes",
        "Documentation": "https://github.com/pmichon/primes#readme",
    },
)
