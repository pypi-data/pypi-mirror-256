from setuptools import setup, find_packages

setup(
    name="akash_package",
    version='0.1',
    packages=find_packages(),
    install_requires = [
        "numpy==1.24.4"
    ],
)