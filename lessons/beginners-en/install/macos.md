# Python install for macOS

Install [Homebrew](http://brew.sh) which makes app and modules installtation
much easier,


Enter this command in the [command line]({{ lesson_url('beginners/cmdline') }}):

```console
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Pnd then you can just enter this command:

```console
$ brew install python3
```

## conda installation

For conda installation use [this link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) and choose Anaconda.

Then you have to add full path to /...../Continuum/anaconda3/Scripts (instead of
dots there will be something different regarding where you installed it) to your environment 
variable PATH - try to find out by yourself (but if you will have some troubles contact us).
You will know that it's been added successfully by typing into your command line:

```bash
conda --help
``` 

After succesfull installation follow how to [create virtual environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)


