"""
Setup script for the perplexity-core package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="perplexity-core",
    version="0.1.0",
    author="holasoymalva",
    author_email="malvabombom@gmail.com",
    description="A base framework for Perplexity API based AI projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/holasoymalva/perplexity-core",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "isort>=5.6.0",
            "flake8>=3.8.0",
            "python-dotenv>=0.15.0",
        ],
    },
)