from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="FastKmedoids",
    version="0.0.6",
    author="Fabio Scielzo Ortiz",
    author_email="fabioscielzo98@gmail.com",
    description="This is a package for applying a fast version of the clustering Kmedoids algorithm, which is build on the Gower Generalized distances, already available in PyDistances package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FabioScielzoOrtiz/FastKmedoids_Package",  # add your project URL here
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['polars','numpy'],
    python_requires=">=3.7"
)