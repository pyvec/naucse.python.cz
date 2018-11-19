# Git

Another program we will install and that will later enable us to cooperate
on emerging programs with others.
It's called Git.
Let's install and set it up.

Installation is different for different operating systems, choose yours.


## Linux

We can install Linux on one command:

**Fedora, RHEL**:

```console
$ sudo dnf install git git gui nano
```

**Ubuntu, Debian**:

```console
$ sudo apt-get install git git-gui nano
```

If you are using some other distribution we expect that you already know
how to install programs. So install *git*,
*gitk*, *git gui* and *nano*.

If you have installed git now set the Git editor.
If you do not like Vim (or you do not know what it is)
enter this command:

```console
$ git config - global core.editor nano
```

Continue with the general [settings](#config) below.


## Windows

Go to [git-scm.org](https://git-scm.org), download
Git and install it.
When installing, select these options:

* Run Git from the Windows Command Prompt
* Checkout Windows-style, commit Unix-style line endings

Do not change other options.

Then set the Git editor.
If you have an open command line, close it and open a new one.
(Installation changes the system settings which have to be loaded again.)
In the new command line, enter:

```console
> git config - global core.editor notepad
> git config --global format.commitMessageColumns 80
> git config - global gui.encoding utf-8
```

Now go to [Settings](#config) below.


## macOS

Run the `git`  in the command line.
If it's already installed, you'll learn how to use it.
Otherwise, install it with Homebrew:

```console
$ brew install git
```

It is still necessary to set up Git editor (enter `nano`,
even if you installed for example Atom during the installation of the editor).
You can do it with this command:

```console
$ git config - global core.editor nano
```

Continue with the general settings:


{{ anchor('config') }}
## Settings

There can be more collaborators in one
project in Git.
To find out who did specific change we need to
tell Git our name and e-mail.
At the command prompt, enter the following commands, but change the
name and address:

```console
$ git config --global user.name "Adéla Novotná"
$ git config --global user.email adela.novotna@example.com
```

You can of course use a nickname or even
fake email, but it will be more complicated to
engage in team projects.
Anyway, your name and email can be changed at any time
by typing the configuration commands again.

> [note]
> If you are afraid of spam, do not worry.
> E-mail can display only people who download the project,
> to which you contributed.
> Spammers mostly focus on less technically capable
> people than Git users. :)

You can also set up color listings - if you don't think
(like some Git authors) that the command line should be black and white:

```console
$ git config --global color.ui true
```

> [note]
> Running `git config` does not print any message that the operation was successful.
> This is normal; there are a lot of other commands, like `cd`.
>
> You can check the current git configuration with the command:
>
> ```console
> $ git config --global --list
> user.name=Adéla Novotná
> user.email=adela.novotna@example.com
> ```

And that's all! You have Git installed. Congratulations!