import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="density",
    version="1.0.0",
    description="Specifications of parametric density functions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/density",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    packages=["density",
              ],
    test_suite='pytest',
    tests_require=['pytest','scipy'],
    include_package_data=True,
    install_requires=['pydantic'],
    entry_points={
        "console_scripts": [
            "density=density.__main__:main",
        ]
    },
)
