from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    # Basic package information:
    name="CAMELSprofiles",
    version="0.1",
    packages=find_packages(),

    # Package metadata:
    author="Richard Stiskalek",
    author_email="richard.stiskalek@protonmail.com",
    description="Density profiles in CAMELS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Richard-Sti/CAMELSprofiles",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "numpy",
        "matplotlib",
        "ipympl",
        "scipy",
        "tqdm",
        "h5py",
        "scienceplots",
        ],
)
