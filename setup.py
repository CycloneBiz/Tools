import setuptools

# Get requirements
with open("requirements.txt") as f:
    req = f.read().splitlines()

# Get markdown
with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="cyclonetools",
 
    version="1.0",
 
    author="Cyclone Communications",
 
    author_email="hello@cyclone.biz",
 
    description="Upload plugins to OpenLoop MongoDB server",

    long_description=long_description,
    long_description_content_type="text/markdown",
 
    url="",
    
    packages=["cyclonetools"],
 
    install_requires=req,
 
    license="MIT",
 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'cyclone=cyclonetools.cli:main'
        ]
    },
)