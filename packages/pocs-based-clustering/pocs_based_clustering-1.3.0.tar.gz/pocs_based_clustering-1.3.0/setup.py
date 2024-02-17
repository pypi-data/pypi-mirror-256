import setuptools
from setuptools import setup


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="pocs_based_clustering",
    version="1.3.0",
    author="Le-Anh Tran",
    author_email="leanhtran@mju.ac.kr",
    description="Official Implementation of POCS-based Clustering Algorithm",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/tranleanh/pocs-based-clustering",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ),
)