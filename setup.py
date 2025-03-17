from setuptools import setup, find_packages

setup(
    name="ad_bs_converter",
    version="0.1.3",
    description="A Python package that converts between the Nepali (Bikram Sambat) and Gregorian (AD) calendars. This tool is useful for applications that require date conversion between these two calendar systems commonly used in Nepal. The package includes functionality to convert a given AD date to the corresponding BS date and vice versa.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/invincibleaayu/ad-bs-converter",
    author="Aayush Dip Giri",
    author_email="your-email@example.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.10.6",
        "setuptools>=76.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    include_package_data=True,
)
