import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hello_world_prod_vk",
    version="0.0.1",
    author="Vasili Kamisarau",
    author_email="vasili_kamisarau@epam.com",
    description="A Hello World package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vasilik23/sample-pypi-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
