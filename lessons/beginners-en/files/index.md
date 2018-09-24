# Files

This section covers how to read from files in Python 
and how to write to them.

You need three steps to read text from a file:
* *open* the file,
* *read* something from it,
* and *close* it finally.

Create a `poem.txt` file in the editor and write any poem to it.
Save the file.

> [note]
> I recommend to use the same editor that you use for your 
> Python program to edit the file with the poem.
>
> If you use a different editor than Atom, be sure to keep in mind when coding:
> * If the editor offers you a choice of encoding, choose `UTF-8`.
> * If `UTF-8 without BOM` is available, use it.
> * If you have to use Notepad then use the non-standard `utf-8-sig` instead.
>
> The [`utf-8`] is the name of the standard encoding.
> You can store any emoji or accented characters to files with this encoding.
> 🎉

[`utf-8`]: https://en.wikipedia.org/wiki/UTF-8

Write this program:

```python
poem_file = open('poem.txt', encoding='utf-8')
content = poem_file.read()
print(content)
poem_file.close()
```

Run it in the directory with `poem.txt`. In other words, the current working 
directory must contain the file with the poem. 

The program prints the poem!

What's going on here?
The `open()` function returns the value that represents the *open file*.
This value has its own methods.
We are using the `read()` method that reads the entire contents 
of the file at once and returns it as a string.
We will cover `close()` that that closes the open file later.


## Iteration over files

You can use open files with the `for` statement. 
It similar as with strings or ranges.
`for i in range` provides consecutive numbers. 
`for c in 'abcd'` provides single string characters. 
`for line in poem_file` provides individual lines read from to the `line` variable.

For example, we can indent the poem to make it stand out of the text.

```python
print('I heard this poem:')
print()
poem_file = open('poem.txt', encoding='utf-8')
for line in poem_file:
    print('    ' + line)
poem_file.close()
print()
print('How do you like it?')
```


When you try it, you will find that it the spacing is not how it should be. 
Are you going to try to explain why this is so?

{% filter solution %}
Each row ends with a newline character (`'\n'`).
When iterating over a Python file, 
this character remains at the end of the string `line` ¹.
The `print()` function then adds another newline character. 
This function always ends the line. 
You can suppress it using the argument `end=''`).
That is one way how to „fix“ this extra spacing. 
The other is to use the method `rstrip()` for each line. 
This method removes all spaces and newline characters 
that are the end of the string.

---

¹  Why it is not removed? If the `'\n'` at the end of line was missing, 
it would not be possible to know if the last line ends with `'\n'` or not.

{% endfilter %}


## Closing files

It is quite important to close the file when the program stops to use it. 
The `close()` method does it.
Operating systems have limits on open files.
If you do not close them you can exceed this limit.
Besides, on Windows, you can not open the file that is still open again.

You can compare files to a fridge: if you want to put something to the fridge, 
you need to open it and then close it.
It works without closing too but then something gets rotten. 

It is easy to forget to close a file.
For example, an exception or `return` statement inside 
the file processing skips the `close()`.
Then the file remains open.

We can use the `try/finally` statement to make sure that the file is closed.

The `finally` block (the statements(s) after `finally`) is always executed.
It executes no matter if the `try` blocks ends with success, 
or with an exception, or you jump out of it using `return` or `break`.

```python
def initial_character():
    """Return the first character in the poem."""

    poem_file = open('poem.txt', encoding='utf-8')
    try:
        content = poem_file.read()
        return content[0]
    finally:
        poem_file.close()

print(initial_character())
```

You can use the `finally` block every time you need 
o close or terminate something - not just a file but
it can be a database connection.


## The `with` statement

Because the `try/finally` block is quite verbose, 
there is a better way in Python. It is the `with` statement:

```python
def initial_character():
    """Return the first character in the poem."""

    with open('poem.txt', encoding='utf-8') as poem_file:
        content = poem_file.read()
        return content[0]

print(initial_character())
```

We used this statement for testing before. 
It wrapped a block with an expected exception.
It checks if the correct exception has occurred 
after the block ends.
In our case, the file is closed when the block ends
no matter what has happened.
The file is closed in all cases - 
when the `with` block ends with success, 
or with an exception or jumping out of it.

The `with` statement is the best option for working with files
in the majority of cases.


## Writing to files

> [warning] Caution!
> It is not a problem to delete or overwrite any file in Python.
> Try following examples in a directory where you have nothing important!

You can write to file in Python.
You need to open a file for writing using a named argument
`mode='w'` (`w` stands for *write*).
You can write individual strings using the `write()` method.

If the file already exists, the open with `mode='w'` overwrites 
its original content. There will be only the text that your program 
writes into it.

```python
with open('second-poem.txt', mode='w', encoding='utf-8') as poem_file:
    poem_file.write('Our old chiming clock\n')
    poem_file.write("Are beating four o'clock\n")
```

> [note] Why there is `\n`?
> The `write()` method does not put a line ending after the string.
> If you need to write multiple lines to the files, you need to need 
> end each of them by newline character `'\n'`. We have described it
> in the [Strings section](../str/).

Or, you can use the `print()` function.
It writes to the terminal by default. 
It can write into an open file if you use a named argument `file`.

Other `print()` options remain unchanged. These options include
line ending, conversion to strings, and printing multiple arguments at a time.

```python
with open('second-poem.txt', mode='w', encoding='utf-8') as poem_file:
    print('Our old chiming clock', file=poem_file)
    print('Are beating', 2+2, "o'clock", file=poem_file)
```
