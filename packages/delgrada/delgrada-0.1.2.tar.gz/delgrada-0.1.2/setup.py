from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="delgrada",
    version="0.1.2",
    description="Lightweight, minimal tensor-/scalar- based autograd engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perceptronv/delgrada/",
    author="Yiding Song",
    author_email="perceptronv@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="autograd, deep-learning, mathematics, education",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=["numpy"],
    project_urls={
        "Source": "https://github.com/perceptronv/delgrada/",
    },
)
