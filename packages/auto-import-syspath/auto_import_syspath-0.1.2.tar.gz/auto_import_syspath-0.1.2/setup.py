from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1.2'
DESCRIPTION = ''
LONG_DESCRIPTION = 'A script that import a path with the relative namepath'

# Setting up
setup(
    name="auto_import_syspath",
    version=VERSION,
    author="nyck_dev (Nycolas Galdino)",
    author_email="<nycolaspimentel12@gmail.com>",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ['packages = packages.auto_import_path:main']},
    keywords=['python', 'auto_import', 'path', 'import_path'],
    classifiers=[
        "Development Status :: 1 - Planning", "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)