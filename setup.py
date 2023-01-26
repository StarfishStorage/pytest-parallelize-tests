import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-parallelize-tests",
    author="Starfish Storage Corporation",
    author_email="rkujawa@starfishstorage.com",
    maintainer="Radek Kujawa",
    maintainer_email="rkujawa@starfishstorage.com",
    license="MIT",
    url="https://github.com/StarfishStorage/pytest-parallelize-tests",
    description='pytest plugin that parallelizes test execution across multiple hosts',
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_parallelize_tests"],
    python_requires=">=3.7",
    install_requires=["pytest>=3.5.0", "redis"],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["parallelize_tests = pytest_parallelize_tests"]},
)
