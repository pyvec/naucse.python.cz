## Packaging

The Setuptools toolkit, and the older Distutils, for distributing Python packages makes it easy to write install scripts in Python. You can use these scripts to build archive files for distribution, which the programmer (user) can then use for compiling and installing your libraries.


Simple example:

```
from setuptools import setup

setup(name='Hello',
      version='1.0',
      description='A simple example',
      author='Lumir Jasiok',
      py_modules=['hello'])
```

Now, you can simply execute 

```
python setup.py build
```

Expected output:

```
running build
running build_py
creating build
creating build/lib
copying hello.py -> build/lib
```

Now, you can find **hello.py** inside build directory.

Other commands, that are interesting for you are:

```
python setup.py sdist
```

This command will create source package, that can be shipped independendly on architecture.

```
python setup.py bdist
```

This command will build "built distribution" package, you can think about it as "binary package" for your platform. By default, bdist will create package in .egg format. This can be placed in private pypi registry and used to distribute python packages internally.

There is also possibility to build RPM packages like this:

```
python setup.py bdist --format=rpm
```

Other possible options are:

|  Format | Description  |
|---|---|
|  gztar  | gzipped tar file (.tar.gz)  |
|  ztar |  compressed tar file (.tar.Z) |
| tar  | tar file (.tar)  |
| zip  | zip file (.zip)  |
| rpm  | RPM  |
| pkgtool  | Solaris pkgtool  |
| sdux  | HP-UX swinstall  |
| wininst  | self-extracting ZIP file for Windows  |
| msi  | Microsoft Installer  |


### setup.py

Setup.py example:

```
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "an_example_pypi_project",
    version = "0.0.4",
    author = "Andrew Carter",
    author_email = "andrewjcarter@gmail.com",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
```

#### Directory structure

```
some_root_dir/
|-- README
|-- setup.py
|-- an_example_pypi_project
|   |-- __init__.py
|   |-- useful_1.py
|   |-- useful_2.py
|-- tests
|-- |-- __init__.py
|-- |-- runall.py
|-- |-- test0.py

```

#### Classifiers

[Python Classifiers](http://pypi.python.org/pypi?%3Aaction=list_classifiers)

Example:

```
Development Status :: 1 - Planning
Development Status :: 2 - Pre-Alpha
Development Status :: 3 - Alpha
Development Status :: 4 - Beta
Development Status :: 5 - Production/Stable
Development Status :: 6 - Mature
Development Status :: 7 - Inactive
Environment :: Console
Environment :: Console :: Curses
Environment :: Console :: Framebuffer
Environment :: Console :: Newt
Environment :: Console :: svgalib
```

To see all commands type:

```
python setup.py --help-commands
Standard commands:
  build             build everything needed to install
  build_py          "build" pure Python modules (copy to build directory)
  build_ext         build C/C++ extensions (compile/link to build directory)
  build_clib        build C/C++ libraries used by Python extensions
  build_scripts     "build" scripts (copy and fixup #! line)
  clean             clean up temporary files from 'build' command
  install           install everything from build directory
  install_lib       install all Python modules (extensions and pure Python)
  install_headers   install C/C++ header files
  install_scripts   install scripts (Python or otherwise)
  install_data      install data files
  sdist             create a source distribution (tarball, zip file, etc.)
  register          register the distribution with the Python package index
  bdist             create a built (binary) distribution
  bdist_dumb        create a "dumb" built distribution
  bdist_rpm         create an RPM distribution
  bdist_wininst     create an executable installer for MS Windows
  check             perform some checks on the package
  upload            upload binary package to PyPI

Extra commands:
  alias             define a shortcut to invoke one or more commands
  bdist_egg         create an "egg" distribution
  develop           install package in 'development mode'
  dist_info         create a .dist-info directory
  easy_install      Find/get/install Python packages
  egg_info          create a distribution's .egg-info directory
  install_egg_info  Install an .egg-info directory for the package
  rotate            delete older distributions, keeping N newest files
  saveopts          save supplied options to setup.cfg or other config file
  setopt            set an option in setup.cfg or another config file
  test              run unit tests after in-place build
  upload_docs       Upload documentation to PyPI
  nosetests         Run unit tests using nosetests

usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
   or: setup.py --help [cmd1 cmd2 ...]
   or: setup.py --help-commands
   or: setup.py cmd --help
```

#### .pypirc

In order to interact with pypi, you first need to setup an account. Go to http://pypi.python.org/pypi and click on Register.

Now, once registered, when you run setup.py commands that interact with pypi you’ll have to enter your username and password each time.

To get around this, place a .pypirc file in your $HOME directory on linux. On windows, an you’ll need to set a HOME environ var to point to the directory where this file lives.

The structure of a .pypirc file is pretty simple:

```
[pypirc]
servers = pypi
[server-login]
username:your_awesome_username
password:your_awesome_password
```

#### Registering Your Project

```
python setup.py register
```

#### Uploading Your Project

Use bdist command:

```
python setup.py bdist_egg
python setup.py bdist_wininst
python setup.py sdist
python setup.py upload
```
