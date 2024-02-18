from setuptools import setup, find_packages
import os
from pathlib import Path
os.path.dirname(os.path.abspath('__file__'))
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="nxfern2",
    version="1.3",
    author="Nicolas Fernandez",
    author_email="",
    description="Demo package",
    url="",
    license="MIT",
    install_requires=[],
    packages=find_packages(),
    long_description='This is a long description',
    long_description_content_type='text/markdown'
)

