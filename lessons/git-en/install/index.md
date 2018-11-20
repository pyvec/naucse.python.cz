# Git

There is another program that we will install and that will later let us cooperate
and develop programs together with other people. It's called Git.
Let's install it and set it up.

The installation procedure is different for different operating systems, so choose yours.


## Linux

In Linux, we can install it with one command:

**Fedora, RHEL**:

```console
$ sudo dnf install git git gui nano
```

**Ubuntu, Debian**:

```console
$ sudo apt-get install git git-gui nano
```

If you are using some other distribution we expect that you already know
how to install programs. Go ahead and install *git*, *gitk*, *git gui* and *nano*.

After you have installed git, choose your Git editor.
If you do not like Vim (or you do not know what it is)
enter this command to choose a more user-friendly editor called Nano:

```console
$ git config - global core.editor nano
```

Continue with the general [settings](#config) below.


## Windows

Go to [git-scm.org](https://git-scm.org), download Git and install it.
When installing, select these options:

* Run Git from the Windows Command Prompt
* Checkout Windows-style, commit Unix-style line endings

Do not change any other options.

Then set your Git editor.
If you have a terminal window open, close it, and open a new one.
(The installation changes system settings which have to be loaded again.)
In the new command line, enter:

```console
> git config - global core.editor notepad
> git config --global format.commitMessageColumns 80
> git config - global gui.encoding utf-8
```

Now go to [Settings](#config) below.


## macOS

Try to run `git` on the command line.
If it's already installed, it will show you how to use it.
Otherwise, install it using Homebrew:

```console
$ brew install git
```

It is still necessary to set up your Git editor (enter `nano`,
even if you installed for example Atom during the installation of the editor).
You do that with this command:

```console
$ git config - global core.editor nano
```

Continue with the general settings:


{{ anchor('config') }}
## Settings

Several people can collaborate in one project in Git.
To track who make a specific change, we need to
tell Git our name and e-mail.
At the command prompt, enter the following commands, but change the
name and address to yours:

```console
$ git config --global user.name "Adéla Novotná"
$ git config --global user.email adela.novotna@example.com
```

You can of course use a nickname or even
fake email, but then it will be more complicated to
engage in team projects.
Anyway, your name and email can be changed at any time
by typing the configuration commands again.

> [note]
> If you are afraid of spam, do not worry.
> Your e-mail address can be viewed only by people who download the project
> to which you contributed.
> Spammers mostly focus on less technically capable people than Git users. :)

You can also set up color listings - if you don't think
(like some Git authors) that the command line should be black and white:

```console
$ git config --global color.ui true
```

> [note]
> Running `git config` does not print any message that the operation was successful.
> This is normal; many other commands behave like that, for example `cd`.
>
> You can check your current git configuration with the command:
>
> ```console
> $ git config --global --list
> user.name=Adéla Novotná
> user.email=adela.novotna@example.com
> ```

And that's all! You have installed Git. Congratulations!
