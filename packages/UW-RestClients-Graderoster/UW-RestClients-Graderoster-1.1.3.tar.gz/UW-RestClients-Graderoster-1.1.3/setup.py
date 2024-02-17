import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients-graderoster>`_.
"""

version_path = 'uw_sws_graderoster/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/uw-restclients-graderoster"
setup(
    name='UW-RestClients-Graderoster',
    version=VERSION,
    packages=['uw_sws_graderoster'],
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'UW-RestClients-Core~=1.4',
        'UW-RestClients-SWS~=2.4',
        'UW-RestClients-PWS~=2.1',
        'mock',
        'lxml~=4.9',
        'Jinja2',
    ],
    license='Apache License, Version 2.0',
    description=(
        'A library for connecting to the SWS Graderoster API at the '
        'University of Washington.'
    ),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
