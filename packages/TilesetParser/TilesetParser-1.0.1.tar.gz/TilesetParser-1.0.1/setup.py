from setuptools import setup, find_packages

setup(
    name='TilesetParser',
    version='1.0.1',
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
