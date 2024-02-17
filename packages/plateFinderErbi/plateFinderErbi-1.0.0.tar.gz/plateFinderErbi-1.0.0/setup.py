from setuptools import setup, find_packages

setup(
    name="plateFinderErbi",
    version='1.0.0',
    author="Erbi Bitri",
    author_email="<mail@gmail.com>",
    description='A package find the plate',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["openpyxl", "pandas", "pyarrow"],
    keywords=[ 'plateFinderErbi', 'pythonsdaal', 'plate', 'sda', 'SDA'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)