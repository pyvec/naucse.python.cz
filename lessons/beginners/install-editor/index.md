# Editor installation

An editor is a program for editing plain text. It is an essential tool for 
every programmer.

It doesn't matter which editor you use, just don't use
Notepad, TextEdit, Word, or Writer.
If you already have some favourite, it will just need to be set up.


## What can editors for programmers do?

Editors for programmers let us edit *plain text*. Unlike programs such as Word, 
Writer, or Pages, it does not let us *format* text.

Since we use the editor to enter commands for the computer, we do not need any formatting, 
we just want to use some of their built-in tricks:
* Multiple file support – useful for larger projects with multiple files
* Line numbering – each line shows the number. Great for debugging
* Offset – (indentation) Very important in Python.
* Coloring – custom code highlighting helps with readability. 



> [note]
>
> That's what a piece of code looks like in the editor:
>
> ```python
>     1  @app.route('/courses/<course:course>/')
>     2  def course_page(course):
>     3      try:
>     4          return render_template(
>     5              'course.html',
>     6              course=course,
>     7              plan=course.sessions,
>     8          )
>     9      except TemplateNotFound:
>    10          abort(404)
> ```


## Choosing and setting up an editor

We recommend using *Atom* for now.

* [Atom]({{ subpage_url('atom') }}) 

You will already have some editor on Linux (but you can always download Atom).
Just try to type into your command line `gedit` or `kate`, and if an editor 
opens, that's your default Linux editor.

* [Gedit]({{ subpage_url('gedit') }}) – GNOME.
* [Kate]({{ subpage_url('kate') }}) – KDE.



### IDE

Most Python programmers use complex and extremely powerful programs, so-called `IDEs` 
(*Integrated Development Environments*),
such as [PyCharm], [Eclipse] or [KDevelop].
But they are not very suitable for beginners.

If you want to use an IDE, you should really know it well. And also keep in mind
that every coach knows only that one IDE that they use most often, so they might not
be able to help you with another.

[PyCharm]: https://www.jetbrains.com/pycharm/
[Eclipse]: https://eclipse.org/
[KDevelop]: https://www.kdevelop.org/

