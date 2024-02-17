# setup.py
# ---------

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("license.txt", "r", encoding="utf-8") as fh:
    license_text = fh.read()

setup(
    name="MediaSwiftPy",
    version="2.1.1",
    author="ROHIT SINGH",
    author_email="rs3232263@gmail.com",
    description="A PYTHON PACKAGE FOR VIDEO CONVERSION AND PROBING USING MediaSwiftPy FFPLAY AND FFPROBE.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ROHIT-SINGH-1",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_data={
        "MediaSwiftPy": ["bin/*"],
    },
    entry_points={
        "console_scripts": [
            "ffpe = MediaSwiftPy.ffpe:ffpe",
            "ffpr = MediaSwiftPy.ffpr:ffpr",
            "ffpl = MediaSwiftPy.ffpl:ffpl",
        ],
    },
    python_requires=">=3.9",
    license="GPL-3.0",  # Specify the correct identifier for GNU GPL version 3
)
