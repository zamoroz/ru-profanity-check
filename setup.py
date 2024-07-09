import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt") as req:
    requirements = req.read().split()


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


transformers_files = package_files(
    'profanity_protector/data/model')

setuptools.setup(
    name="ru-profanity-protector",
    version="1.0.0",
    author="Andrey Morozov",
    author_email="back@laconism.pro",
    description="An even more robust fork of 'profanity-check'.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zamoroz/ru-profanity-protector",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    package_data={'profanity_protector': transformers_files},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
