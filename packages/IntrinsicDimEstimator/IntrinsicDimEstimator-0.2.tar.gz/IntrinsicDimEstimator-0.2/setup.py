from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.2'
DESCRIPTION = 'Intrinsic Dimensionality Estimation'
LONG_DESCRIPTION = (
    'A package for estimating the intrinsic dimensionality of a dataset. '
    'Supports multiple estimation methods including Correlation Dimension, '
    'Nearest Neighbor Dimension, Packing Numbers, Geodesic Minimum Spanning Tree, '
    'Eigenvalue Analysis, and Maximum Likelihood Estimation.'
)

# Setting up
setup(
    name="IntrinsicDimEstimator",
    version=VERSION,
    author="Eng. Alberto Biscalchin",
    author_email="<biscalchin.mau.se@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'scipy',
        'matplotlib'
    ],
    keywords=[
        "intrinsic dimensionality", "dimensionality estimation", "data analysis", "machine learning"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
