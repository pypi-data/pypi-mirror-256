#!/usr/bin/env python
 
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
from apkpatcher import conf


setup(
    name='apkpatcher',
    version=conf.VERSION,
    packages=['apkpatcher'],
    author="MadSquirrel",
    author_email="benoit.forgette@ci-yow.com",
    description="""Tool use as library or in cli to patch an APK, inject some libraries inside the APK or add a custom certificate""",
    package_data={'apkpatcher': []},
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    download_url="https://gitlab.com/MadSquirrels/mobile/apkpatcher",
    include_package_data=True,
    url='https://ci-yow.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning"
    ],
 
    entry_points = {
        'console_scripts': [
            'apkpatcher=apkpatcher:main',
        ],
    },
    cmdclass={
    },
    install_requires = [
        'sty',
        'pyaxml==0.0.5',
        'androguard==4.0.2',
    ],
    python_requires='>=3.5'
 
)
