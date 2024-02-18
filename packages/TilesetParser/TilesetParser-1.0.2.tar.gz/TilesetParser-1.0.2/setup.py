from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='TilesetParser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.4',
        'opencv-python==4.9.0.80'
    ],
    entry_points={
        'console_scripts': [
            'tilesetparser=TilesetParser.main:main',
        ],
    },
)
