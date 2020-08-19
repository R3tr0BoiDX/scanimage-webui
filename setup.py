#!/usr/bin/python3
from setuptools import setup, find_packages

packages = find_packages()
print("Packages: {}".format(packages))

REQUIREMENTS_TXT = "./requirements.txt"
with open(REQUIREMENTS_TXT, "r") as file:
    INSTALL_REQUIRES = [line.strip() for line in file]

print("Requirements: {}".format(INSTALL_REQUIRES,))

setup(
    name='ScanImage WEB UI',
    version='1.0.0',
    url='',
    license='MIT',
    author='Ales Adamek',
    author_email='alda78@seznam.cz',
    description='WEB UI for SANE scanimage command',
    packages=packages,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,  # MANIFEST.in
    zip_safe=False,  # aby se spravne vycitala statika pridana pomoci MANIFEST.in
    entry_points={
        'console_scripts': [
            'scanimage-webui=scanimage_webui.main:main',
        ],
    },
)
