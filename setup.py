# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

from innaterapluginio import (
    __author__,
    __description__,
    __email__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from innaterapluginio.dependencies import get_pip_dependencies

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=open("README.md").read(),
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    install_requires=get_pip_dependencies(),
    python_requires=">=3.6",
    packages=find_packages(include=["innaterapluginio", "innaterapluginio.*"]),
    package_data={
        "innaterapluginio": [
            "assets/system/99-innaterapluginio-udev.rules",
            "project/integration/tpls/*/*.tpl",
            "project/integration/tpls/*/.*.tpl",  # include hidden files
            "project/integration/tpls/*/.*/*.tpl",  # include hidden folders
            "project/integration/tpls/*/*/*.tpl",  # NetBeans
            "project/integration/tpls/*/*/*/*.tpl",  # NetBeans
        ]
    },
    entry_points={        
        "console_scripts": [
            "innaterapluginio = innaterapluginio.__main__:main",
            "innio = innaterapluginio.__main__:main",
            "inniodebuggdb = innaterapluginio.__main__:debug_gdb_main",
        ]    
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Compilers",
    ],
    keywords=[
        "iot",
        "embedded",
        "arduino",
        "mbed",
        "esp8266",
        "esp32",
        "fpga",
        "firmware",
        "continuous-integration",
        "cloud-ide",
        "avr",
        "arm",
        "ide",
        "unit-testing",
        "hardware",
        "verilog",
        "microcontroller",
        "debug",
    ],
)
