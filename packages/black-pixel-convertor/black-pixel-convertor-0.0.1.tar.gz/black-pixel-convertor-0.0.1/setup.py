from setuptools import setup, find_packages

setup(
    name="black-pixel-convertor",
    version="0.0.1",
    description="This library change black pixels to invisible.",
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
