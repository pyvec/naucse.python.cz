# Editor installation

Editor is program for editing plain text. It is essential tool for 
every programmer.

It doesn't matter which editor you will use, just don't use
Notepad, TextEdit, Word or Writer.
If you already have some favourite it will just need set up.


## What editors for programmers can do?

Editors for programmers allows us to edit *plain text*. Unlike programs such Word, 
Writer or Pages, it does not allow *formatting* text.

Using the editor, we will enter commands to the computer, so we do not need formatting, 
but we will use some of their built-in tricks:
* Multiple file support – useful for larger projects with multiple files
* Line numbering – each line shows the number. Great for debugging
* Offset – (indentation) Very important in Python.
* Coloring – tailoring code highlight helps with readability. 



> [note]
>
> That's how piece of code looks like in editor:
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


## Choice and setting up an editor

We recommend using *Atom* for now.

* [Atom]({{ subpage_url('atom') }}) 

You will already have some editor on Linux (but you can always download Atom).
Just try to type into your command line `gedit` or `kate` and if some editor 
will open that's your default Linux editor.

* [Gedit]({{ subpage_url('gedit') }}) – GNOME.
* [Kate]({{ subpage_url('kate') }}) – KDE.




### IDE

Most Python programmers use complex and extremely powerful programs, so called `IDEs` 
(*Integrated Development Environments*),
such as [PyCharm], [Eclipse] or [KDevelop].
But they are not much suitable for beginners.

If you want to use some you should really know it. And also keep in mind
that every coach knows only that one which they use often so they might not
be able to help you.

[PyCharm]: https://www.jetbrains.com/pycharm/
[Eclipse]: https://eclipse.org/
[KDevelop]: https://www.kdevelop.org/

