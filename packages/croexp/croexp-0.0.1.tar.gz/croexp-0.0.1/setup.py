from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_descriptionmd = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A package that allows to verify the parameters of a crontab expression.'

# Setting up
setup(
    name="croexp",
    version=VERSION,
    author="Youn99 (Youness Kazize)",
    author_email="<younny7kaziz@gmail.com>",
    description=DESCRIPTION,
    long_description = long_descriptionmd,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['regex'],
    keywords=['python', 'crontab expression'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)