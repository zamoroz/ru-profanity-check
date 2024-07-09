import setuptools
import os
import subprocess
import sys

try:
    import git
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'gitpython'])
    import git

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
    'profanity_check/data/model')


cwd = os.getcwd()
gitdir = os.path.dirname(os.path.realpath(__file__))
os.chdir(gitdir)
g = git.cmd.Git(gitdir)
try:
    g.execute(['git', 'lfs', 'pull'])
except git.exc.GitCommandError:
    raise RuntimeError("Make sure git-lfs is installed!")
os.chdir(cwd)

setuptools.setup(
    name="ru-profanity-check",
    version="1.0.0",
    author="Andrey Morozov",
    author_email="back@laconism.pro",
    description="An even more robust fork of 'profanity-check'.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zamoroz/ru-profanity-check",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    package_data={'profanity_check': ["profanity_check/data/embeddings.txt"] + transformers_files},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
