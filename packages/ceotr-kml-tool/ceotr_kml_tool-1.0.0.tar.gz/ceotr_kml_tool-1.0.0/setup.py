import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ceotr_kml_tool",
    version="1.0.0",
    author="CEOTR",
    description="library tool to download and process KML files from SFMC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.oceantrack.org/ceotr/gliders/kml_tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4',
        'pykml',
    ],
    python_requires='>=3.6',
    package_data={
        # If any package contains *.txt files, include them:
        "kml_tool": ["ref/GEstyle.txt"],
    },
    include_package_data=True,
)
