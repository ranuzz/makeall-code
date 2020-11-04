import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.0.1"

setuptools.setup(
    name="cluedo",
    version=VERSION,
    author="ranuzz",
    author_email="ranuzz@outlook.com",
    description="",
    long_description=long_description,
    url="",
    entry_points = {
        'console_scripts': [
            'cluedo=cluedo.apps.main:run',
            'cluedo-webserver=cluedo.apps.webserver:run'
            ],
    },
    packages=setuptools.find_packages(),
    package_data = {
        'cluedo' : ['cluedo.cfg']
    },
    include_package_data=True,
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)