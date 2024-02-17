from setuptools import setup, find_packages

#setting up
setup(
    name="plateFinderAndi",
    version='1.0.1',
    author="Andi",
    author_email="<mail@gmail.com>",
    description='A package that finds the plate',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["openpyxl", "pandas", "pyarrow"],
    keywords=[ 'plateFinder', 'pythonsdaal', 'plate', 'sda', 'SDA'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)