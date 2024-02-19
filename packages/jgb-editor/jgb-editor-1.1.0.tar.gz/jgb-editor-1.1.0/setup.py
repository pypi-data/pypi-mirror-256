import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="jgb-editor",
    version="1.1.0",
    author="Hwang Dongha",
    author_email="depth221@gmail.com",
    description="A simple Jeongganbo editor",
    license="GPLV3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/depth221/Jeongganbo-editor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)