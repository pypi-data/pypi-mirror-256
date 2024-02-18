import setuptools

setuptools.setup(
    name="laser_pkg",
    version="0.0.2",
    author="JiyunLee",
    author_email="easyun@lgensol.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)