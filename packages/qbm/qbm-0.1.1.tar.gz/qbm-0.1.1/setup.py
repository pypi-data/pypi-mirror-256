import setuptools

# with open("requirements.txt", "r") as requirements_file:
# requirements = requirements_file.read().splitlines()

requirements = [
    "dwave-ocean-sdk>=4.2.0",
    "matplotlib>=3.4.3",
    "numpy>=1.20.3",
    "pandas>=1.3.3",
    "scipy>=1.7.1",
]


setuptools.setup(install_requires=requirements)
