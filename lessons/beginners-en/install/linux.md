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

If there will be "Python" and version lower than 3.3, ask coach.

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


{{ anchor('install-conda') }}
## conda installation

For conda installation use [this link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) and choose Anaconda.

Then you have to add full path to /......./Continuum/anaconda3/Scripts (instead of
dots there will be something different regarding where you installed it)
to your environment variable PATH - try to find out by yourself (but if you will have
some troubles contact us). You will know that it's been added successfully by typing into 
your command line:

```bash
conda --help
``` 


After successful installation follow how to [create virtual environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)


