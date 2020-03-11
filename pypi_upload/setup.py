import re
from os import path

from setuptools import find_packages, setup

project_root = path.join(path.abspath(path.dirname(__file__)), "..")


def get_version():
    with open(
        path.join(project_root, "more_properties", "__init__.py"), encoding="utf-8"
    ) as init_file:
        return re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M
        ).group(1)


def get_requirements():
    with open(
        path.join(project_root, "requirements.txt"), encoding="utf-8"
    ) as requirements_file:
        return list(filter(None, requirements_file.read().splitlines()))


def get_long_description():
    with open(path.join(project_root, "README.md"), encoding="utf-8") as readme_file:
        return readme_file.read()


setup(
    name="more_properties",
    version=get_version(),
    packages=find_packages(include=("more_properties", "more_properties.*")),
    install_requires=get_requirements(),
    setup_requires=["wheel"],
    author="Robert Wright",
    author_email="madman.bob@hotmail.co.uk",
    description="A collection of property variants",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/madman-bob/python-more-properties",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
)
