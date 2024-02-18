try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='bio_volumentations',
    version='1.0.8',
    author='Roman Sol (ZFTurbo), ashawkey, qubvel, muellerdo, Lucia Hradecka',
    packages=find_packages(),
    url='https://gitlab.fi.muni.cz/xdupkan/volumentations/',
    description='Library for 3D augmentations for biomedical images',
    long_description='Library for 3D augmentations for biomedical images. Inspired by albumentations.'
                     'More details: https://gitlab.fi.muni.cz/xdupkan/volumentations/',
    install_requires=[
        'scikit-image',
        'scipy',
        'opencv-python',
        "numpy",
    ],
    entry_points={
        'console_scripts': [
            'bioVolumentation=bio_volumentations:__init__'
        ]
    }
)
