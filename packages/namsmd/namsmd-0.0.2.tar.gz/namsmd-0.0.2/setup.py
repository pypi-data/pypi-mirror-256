from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Sites Media Downloader'
LONG_DESCRIPTION = 'My first Python package to download files from sites'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="namsmd", 
        version=VERSION,
        author="Nam Nguyen",
        author_email="nnamnguyenn@07kpq.onmicrosoft.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['lxml','beautifulsoup4'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            #"Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            #"Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)