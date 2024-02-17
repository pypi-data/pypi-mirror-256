from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Data Protecting Package'
LONG_DESCRIPTION = 'This package helps to protect all the data which you pass to LLM by encoding it first and decoding it afterward.'

# Setting up
setup(
    name="bc-en-de-coder",
    version=VERSION,
    author="Abhishek kumar SIngh",
    author_email="<abhishek123kumar123singh@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['bc-en-de-coder'],
    install_requires=['PyPDF2', 'pyautogui'],
    keywords=['python', 'Data secure', 'Encoder', 'Decoder', 'pdf reader'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)