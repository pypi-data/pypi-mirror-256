import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySCILTagger",
    version="0.0.4",
    author="Mara Schwartz, Jeremy Macks",
    author_email="maraschwartz44@gmail.com, macksj@rpi.edu",
    description="A dialog-act tagger for pySCIL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Malorn44/pySCIL-tagger",
    project_urls={
        "Documentation": "https://github.com/Malorn44/pySCIL-tagger",
        "Source Code": "https://github.com/Malorn44/pySCIL-tagger",
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