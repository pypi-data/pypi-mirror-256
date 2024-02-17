import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySCIL",
    version="0.0.12",
    author="Mara Schwartz, Esteban Castillo Juarez, Ivan Leon",
    author_email="maraschwartz44@gmail.com, castie2@rpi.edu, leoni@rpi.edu",
    description="A sociolinguistics package for NLP research.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Malorn44/pySCIL",
    project_urls={
        "Documentation": "https://github.com/Malorn44/pySCIL",
        "Source Code": "https://github.com/Malorn44/pySCIL",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
)
