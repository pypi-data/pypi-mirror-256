from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="black-pixel-convertor",
    version="0.0.2",
    description="This library change black pixels to invisible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    install_requires=["patchify", "numpy", "pillow"],
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ]
)
