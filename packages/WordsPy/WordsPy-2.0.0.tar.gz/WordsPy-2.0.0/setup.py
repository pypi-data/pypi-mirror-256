from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

VERSION = '2.0.0'
DESCRIPTION = 'Get words for any langauge.'
LONG_DESCRIPTION =description

# Setting up
setup(
    name="WordsPy",
    version=VERSION,
    author="eymenefealtun (Eymen Efe Altun)",
    author_email="<eymenefealtun@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'words', 'extraction', 'word', 'lexicon'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
