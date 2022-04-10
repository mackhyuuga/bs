# Import required functions
from setuptools import setup, find_packages

# pip install -e .           ---->        to install the package

# Call setup function
setup(
    author="Allison Eduardo",
    description="blender particle script",
    name="ps",
    version="0.1.0",
    packages=find_packages(include=["ps", "ps.*"]),
    install_requires=["pandas",
                      "scipy",
                      "pysqlite3"]
)
