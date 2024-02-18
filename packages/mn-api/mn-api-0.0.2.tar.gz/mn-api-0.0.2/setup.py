"""
Setup File for mn-api
"""
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="mn-api",
    version='0.0.2',
    author="EduardoProfe66",
    author_email="eduardoglez64377@gmail.com",
    description="Big sort of numerical methods. Code and docs are in spanish ;)",
    url = "https://github.com/EduardoProfe666/mn-api",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    python_requires=">=3.9, <4",
    install_requires=['numpy', 'matplotlib', 'scipy', 'simpy', 'jupyterlab', 'pandas', 'tabulate'],
    keywords=['numerical methods', 'metodos numericos', 'cujae', 'python', 'jupyter-lab'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)