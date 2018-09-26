## Regular expressions

A regular expression is a special sequence of characters that helps you match or find other strings or sets of strings, using a specialized syntax held in a pattern. Regular expressions are widely used in UNIX world.

The module re provides full support for Perl-like regular expressions in Python. The re module raises the exception re.error if an error occurs while compiling or using a regular expression.

### The match Function

Match syntax

```
re.match(pattern, string, flags=0)
``` 

**pattern** - This is the regular expression to be matched.

**string** - This is the string, which would be searched to match the pattern at the beginning of string.

**flags** - You can specify different flags using bitwise OR (|).

The re.match function returns a match object on success, None on failure. We usegroup(num) or groups() function of match object to get matched expression.

**group(num=0)** - This method returns entire match (or specific subgroup num)

**groups()** - This method returns all matching subgroups in a tuple (empty if there weren't any)

Example:

```
>>> import re
>>>
>>> line = "Cats are smarter than dogs"
>>> matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
>>> matchObj
<re.Match object; span=(0, 26), match='Cats are smarter than dogs'>
>>> if matchObj:
...  print("matchObj.group() : ", matchObj.group())
...  print("matchObj.group(1) : ", matchObj.group(1))
...  print("matchObj.group(2) : ", matchObj.group(2))
... else:
...  print("No match")
...
matchObj.group() :  Cats are smarter than dogs
matchObj.group(1) :  Cats
matchObj.group(2) :  smarter
```

### The search Function

This function searches for first occurrence of RE pattern within string with optional flags.

```
re.search(pattern, string, flags=0)
```

The re.search function returns a match object on success, none on failure. We use group(num) or groups() function of match object to get matched expression.

Example:

```
>>> import re
>>>
>>> line = "Cats are smarter than dogs";
>>>
>>> searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)
>>>
>>> if searchObj:
...  print("searchObj.group() : ", searchObj.group())
...  print("searchObj.group(1) : ", searchObj.group(1))
...  print("searchObj.group(2) : ", searchObj.group(2))
... else:
...  print("Nothing found")
...
searchObj.group() :  Cats are smarter than dogs
searchObj.group(1) :  Cats
searchObj.group(2) :  smarter
```

### Matching Versus Searching

Python offers two different primitive operations based on regular expressions: match checks for a match only at the beginning of the string, while search checks for a match anywhere in the string (this is what Perl does by default).

Example:

```
>>> import re
>>>
>>> line = "Cats are smarter than dogs";
>>>
>>> matchObj = re.match( r'dogs', line, re.M|re.I)
>>>
>>> if matchObj:
...  print("match --> matchObj.group() : ", matchObj.group())
... else:
...  print("No match")
...
No match
>>> searchObj = re.search( r'dogs', line, re.M|re.I)
>>> if searchObj:
...  print("search --> searchObj.group() : ", searchObj.group())
... else:
...  print("Nothing found")
...
search --> searchObj.group() :  dogs
```

### Search and Replace

One of the most important re methods that use regular expressions is sub.

```
re.sub(pattern, repl, string, max=0)
```

This method replaces all occurrences of the RE pattern in string with repl, substituting all occurrences unless max provided. This method returns modified string.

```
>>> import re
>>>
>>> phone = "2004-959-559 # This is Phone Number"
>>> num = re.sub(r'#.*$', "", phone)
>>> print("Phone Num : ", num)
Phone Num :  2004-959-559
>>> num = re.sub(r'\D', "", phone)
>>> print("Phone Num : ", num)
Phone Num :  2004959559
```

First replace deletes Python-style comments, while second remove anything other than digits.

### Regular Expression Modifiers, Option Flags

**re.I** - Performs case-insensitive matching.

**re.M** - Makes $ match the end of a line (not just the end of the string) and makes ^ match the start of any line (not just the start of the string).

**re.S** - Makes a period (dot) match any character, including a newline.

**re.U** - Interprets letters according to the Unicode character set. This flag affects the behavior of \w, \W, \b, \B.

### Regular Expression Patterns

**^** - Matches beginning of line.

**$** - Matches end of line.

**.** - Matches any single character except newline. Using m option allows it to match newline as well.

**\w** - Matches word characters.

**\W** - Matches word characters.

**\s** - Matches whitespace. Equivalent to [\t\n\r\f].

**\S** - Matches nonwhitespace.

**\d** - Matches digits. Equivalent to [0-9].
