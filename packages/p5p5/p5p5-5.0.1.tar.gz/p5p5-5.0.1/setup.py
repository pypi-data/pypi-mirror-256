

import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
name="p5p5",
version="5.0.1",
author="PySimpleSoft Inc.",
author_email="",
install_requires=["PySimpleGUI"],
description="A test upload",
long_description=readme(),
long_description_content_type="text/markdown",
license='Free To Use But Restricted',
keywords="p5p5",
url="http://python.org",
packages=setuptools.find_packages(),
python_requires=">=3.6",
classifiers=[
"Intended Audience :: Developers",
"License :: Other/Proprietary License",
"Operating System :: OS Independent",
"Framework :: PySimpleGUI",
"Framework :: PySimpleGUI :: 5",
"Programming Language :: Python :: 3",
"Programming Language :: Python :: 3.6",
"Programming Language :: Python :: 3.7",
"Programming Language :: Python :: 3.8",
"Programming Language :: Python :: 3.9",
"Programming Language :: Python :: 3.10",
"Programming Language :: Python :: 3.11",
"Programming Language :: Python :: 3.12",
"Programming Language :: Python :: 3.13",
"Topic :: Multimedia :: Graphics",
],
package_data={"": 
["CONTRIBUTING.md","LICENSE.txt"]
        },
entry_points={'gui_scripts': [
"p5p5=p5p5.p5p5:main",
    ]
    },
)

