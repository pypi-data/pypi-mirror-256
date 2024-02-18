import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RHINOpy",
    version="0.0.2",
    author="Moritz Muellerschoen",
    description="Quicksample Test Package for SQLShack Demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    py_modules=["quicksample"],
    package_dir={'RHINOpy':'RHINOpy'},
    install_requires=[
        "numpy",
        "scipy",
        "techmanpy",
        "asyncio",
        "telnetlib3",
        "paho-mqtt",
        "opencv-contrib-python"
    ]
)