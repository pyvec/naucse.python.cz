# Python installation on Linux

Installing Python on Linux is actually easy.
The only difficult part could be that there are many distributions that
needs different installation commands.


## Python 3

First chech in your [command line]({{ lesson_url('beginners/cmdline') }})
if you don't already have python3 installed:

```console
$ python3 --version
```
If there will appear "Python" and version number (e. g. `Python 3.5.2`)
and the version is higher than 3.4 you are done here so continue with
other section [`tkinter` check](#check-tkinter).

If there will be „Python“ and version lower than 3.3, ask coach.

If `bash: python3: command not found` or something similar will appear
you will have to install Python3.
Command depends on your distribution.


* Fedora:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo dnf install python3
  ```
  {% endfilter %}
* Ubuntu:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo apt-get install python3
  ```
  {% endfilter %}

If you are using some other distribution we expect that you already know
how to install programs. If not try to ask Google.


{{ anchor('check-tkinter') }}
## Tkinter check

Some Linux ditros have just some parts of Python.
Most of the time there is no `tkinter` module which will allow us to draw.
So first you will have to check if you already have it or not.

```console
$ python3 -m tkinter
```

If there will appear window everything is fine and you can continue with
[`conda` instalation](#install-conda).

If not you will have to install `tkinter`:

* Fedora:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo dnf install python3-tkinter
  ```
  {% endfilter %}
* **Ubuntu**:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo apt-get install python3-tk
  ```
  {% endfilter %}

If you have other distro check the package name on Google.

{{ anchor('install-conda') }}
## [conda installation]
After succesfull installation follow how to [create virtual environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)

[conda installation]: https://conda.io/docs/user-guide/install/linux.html
