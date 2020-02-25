# Python installation for Windows 

Go to [the Python website](https://www.python.org/downloads/) and 
download the latest stable version of Python. From version 3.6.0.
there are some enhancements for Windows so download only version
 **3.6.0 and above**.

How to know which installer is the right one?
If your computer has 64bit Windows then download *Windows x86-64 executable installer*.
If your Windows is only 32bit download *Windows x86 executable installer*.


> [note]
> If you don't know what Windows version do you have just open **Start**, 
> search **System** and open **System information**.
>
> {{ figure(
    img=static('windows_32v64-bit.png'),
    alt='Windows version',
) }}

Then you can run the installer.
In the beginning check **Install launcher for all Users**
and also **Add Python 3.6 to PATH**.
This will make creating venv much easier.

(If you don't have admin rights don't check *Install launcher for all Users*.)

{{ figure(
    img=static('windows_add_python_to_path.png'),
    alt='Python installation',
) }}

Then click **Install now** and follow the instructions.

If you have your command line open, close it and open again.


## Virtual environment creation

<!-- Pozn. Tahle sekce je velice podobná pro Linux, Mac i Windows;
     měníš-li ji, koukni se jestli není změna potřeba i jinde. -->

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif -%}

Once the Python will be installed, please create virtuall environment.

Choose the folder where you want to have files related to the Tieto Python Academy.
It can be for example `C:\{{ rootname }}`.

Open the command line({{ lesson_url('beginners/cmdline') }})
and using `cd` switch to it.
Create virtual environment:

```dosvenv
> py -3 -m venv venv
```

Directory <code><span class="pythondir">~/{{ rootname }}</span>\venv</code> were created,


## Virtual environment activation

You canenable the virtual environment like this:

<div class="highlight">
<pre><code><span class="gp">&gt;</span> <span class="pythondir">~/{{ rootname }}</span>\venv\Scripts\activate
</code></pre></div>

> [note]
> Don't forgot to enter <span class="pythondir">~/{{ rootname }}</span>
> your directory

You should see
(in front of `>`) you should see word `(venv)`.
That mean that venv is *active*.

