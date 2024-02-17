from setuptools import setup, find_packages

setup(
    name="pypools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "redislite",
    ],
    extras_require={

    }
)