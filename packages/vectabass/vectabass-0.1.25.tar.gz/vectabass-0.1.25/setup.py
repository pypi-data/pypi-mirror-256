from setuptools import setup, find_packages

setup(
    name="vectabass",
    version="0.1.25",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "requests",
        "uvicorn",
    ],
    python_requires=">=3.7",
)
