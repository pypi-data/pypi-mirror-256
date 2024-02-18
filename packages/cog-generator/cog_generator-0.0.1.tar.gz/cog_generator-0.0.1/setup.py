from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cog_generator",
    version="0.0.1",
    description="This package wraps around the native GDAL library which enables Cloud Optimized GeoTiffs generation at ease into your Python projects.",
    author="Raj Bhattarai",
    author_email="raj.bhattarai222@gmail.com",
    packages=find_packages(),
    license="GPLv3",
    url="https://github.com/iamrajbhattarai/cog_generator",
    install_requires=["GDAL>=3.4.1"],
    keywords=["COG", "GeoTiff"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)