## Testing

Different kind of tests:

* Unit tests: Make sure a class or a function works as expected in isolation
* Functional tests: Verify that the service does what it says from the consumer's point of view, and behaves correctly even on bad requests
* Integration tests: Verify how (a service) integrates with all its network dependencies
* Load tests: Measure the service performances
* End-to-end tests: Verify that the whole system works with an end-to-end test

Workflow of testing:

* Think about your new function or method. What feauture should provide?
* Write some skeleton of the code, so your program won't break. Your test should fail, so you are sure, that your test code is able to fail.
* Write dummy code for your skeleton, so your new code will pass the test. It doesn't have to fully functional code.
* Rewrite your code, so it does what suppose to do and make that test(s) passes.

### Example code

**unnecessary_math.py**

```
'''
Module showing how doctests can be included with source code
Each '>>>' line is run as if in a python shell, and counts as a test.
The next line, if not '>>>' is the expected output of the previous line.
If anything doesn't match exactly (including trailing spaces), the test fails.
'''
 
def multiply(a, b):
    """
    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    'aaa'
    """
    return a * b
```

### Type of test

#### doctests

The doctest test framework is a python module that comes prepackaged with Python.

Running doctest:

```
python -m doctest -v <file>
```

```
$ python -m doctest -v unnecessary_math.py
Trying:
    multiply(4, 3)
Expecting:
    12
ok
Trying:
    multiply('a', 3)
Expecting:
    'aaa'
ok
1 items had no tests:
    unnecessary_math
1 items passed all tests:
   2 tests in unnecessary_math.multiply
2 tests in 2 items.
2 passed and 0 failed.
Test passed.
```

Running doctest in seperate file:

**test\_unnecessary\_math.txt**

```
This is a doctest based regression suite for unnecessary_math.py
Each '>>' line is run as if in a python shell, and counts as a test.
The next line, if not '>>' is the expected output of the previous line.
If anything doesn't match exactly (including trailing spaces), the test fails.
 
>>> from unnecessary_math import multiply
>>> multiply(3, 4)
12
>>> multiply('a', 3)
'aaa'
```

Output:

```
$ python -m doctest -v test_unnecessary_math.txt
Trying:
    from unnecessary_math import multiply
Expecting nothing
ok
Trying:
    multiply(3, 4)
Expecting:
    12
ok
Trying:
    multiply('a', 3)
Expecting:
    'aaa'
ok
1 items passed all tests:
   3 tests in test_unnecessary_math.txt
3 tests in 1 items.
3 passed and 0 failed.
Test passed.
```

#### unittest

The unittest test framework is python’s xUnit style framework.
It is a standard module that you already have if you’ve got python version 2.1 or greater.

We will be using same unnecessary_math.py module as earlier.

**test\_um\_unittest.py**

```
import unittest
from unnecessary_math import multiply
 
class TestUM(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_numbers_3_4(self):
        self.assertEqual( multiply(3,4), 12)
 
    def test_strings_a_3(self):
        self.assertEqual( multiply('a',3), 'aaa')
 
if __name__ == '__main__':
    unittest.main()
```

Run code:

```
$ python test_um_unittest.py -v
test_numbers_3_4 (__main__.TestUM) ... ok
test_strings_a_3 (__main__.TestUM) ... ok
```

### Nose

Nose’s tagline is “nose extends unittest to make testing easier”.
It’s is a fairly well known python unit test framework, and can run doctests, unittests, and “no boilerplate” tests.

You have to install nose:

```
pip install nose
```

Example:

**test_um_nose.py**

```
from unnecessary_math import multiply
 
def test_numbers_3_4():
    assert multiply(3,4) == 12 
 
def test_strings_a_3():
    assert multiply('a',3) == 'aaa' 
```

Run code:

```
$ nosetests -v test_um_nose.py
test_um_nose.test_numbers_3_4 ... ok
test_um_nose.test_strings_a_3 ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.003s

OK
```

Nose extends unittests possibilities. We can add specific code to run:

* at the beginning and end of a module of test code (setup_module/teardown_module)
To get this to work, you just have to use the right naming rules.

* at the beginning and end of a class of test methods (setup_class/teardown_class)
To get this to work, you have to use the right naming rules, and include the ‘@classmethod’ decorator.

* before and after a test function call (setup_function/teardown_function)
You can use any name. You have to apply them with the ‘@with_setup’ decorator imported from nose.
You can also use direct assignment, which I’ll show in the example.

* before and after a test method call (setup/teardown)
To get this to work, you have to use the right name.


Full example:

```
from nose import with_setup # optional

from unnecessary_math import multiply

def setup_module(module):
    print("") # this is to get a newline after the dots
    print("setup_module before anything in this file")

def teardown_module(module):
    print("teardown_module after everything in this file")

def my_setup_function():
    print("my_setup_function")

def my_teardown_function():
    print("my_teardown_function")

@with_setup(my_setup_function, my_teardown_function)
def test_numbers_3_4():
    print('test_numbers_3_4  <============================ actual test code')
    assert multiply(3,4) == 12

@with_setup(my_setup_function, my_teardown_function)
def test_strings_a_3():
    print('test_strings_a_3  <============================ actual test code')
    assert multiply('a',3) == 'aaa'


class TestUM:

    def setup(self):
        print("TestUM:setup() before each test method")

    def teardown(self):
        print("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print("setup_class() before any methods in this class")

    @classmethod
    def teardown_class(cls):
        print("teardown_class() after any methods in this class")

    def test_numbers_5_6(self):
        print('test_numbers_5_6()  <============================ actual test code')
        assert multiply(5,6) == 30

    def test_strings_b_2(self):
        print('test_strings_b_2()  <============================ actual test code')
        assert multiply('b',2) == 'bb'
```

Result:

```
$ nosetests -s test_um_nose_fixtures.py

setup_module before anything in this file
setup_class() before any methods in this class
TestUM:setup() before each test method
test_numbers_5_6()  <============================ actual test code
TestUM:teardown() after each test method
.TestUM:setup() before each test method
test_strings_b_2()  <============================ actual test code
TestUM:teardown() after each test method
.teardown_class() after any methods in this class
my_setup_function
test_numbers_3_4  <============================ actual test code
my_teardown_function
.my_setup_function
test_strings_a_3  <============================ actual test code
my_teardown_function
.teardown_module after everything in this file

----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```

#### pytest

First, you have to install pytest:

```
pip install pytest
```

Unit test counterpart code:

```
import unittest
from unnecessary_math import multiply
 
class TestUM(unittest.TestCase):
 
    def test_numbers_3_4(self):
        self.assertEqual( multiply(3,4), 12)
```

Pytest version:

```
from unnecessary_math import multiply
 
def test_numbers_3_4():
    assert( multiply(3,4) == 12 )
```

There is no need to import unnittest.

There is no need to derive from TestCase.

There is no need to for special self.assertEqual(), since we can use Python’s built in assert statement.

**test_um_pytest.py**

```
from unnecessary_math import multiply
 
def test_numbers_3_4():
    assert multiply(3,4) == 12 
 
def test_strings_a_3():
    assert multiply('a',3) == 'aaa' 
```

Run tests:

```
python -m pytest -v test_um_pytest.py
py.test -v test_um_pytest.py
```

Result:

```
py.test -v test_um_pytest.py
============================================================================================================ test session starts =============================================================================================================
platform darwin -- Python 3.7.0, pytest-3.8.0, py-1.6.0, pluggy-0.7.1 -- /Users/jasiplum/Development/Projects/Tieto/Python/naucse/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/jasiplum/Development/Projects/Tieto/Python/naucse, inifile:
collected 2 items

test_um_pytest.py::test_numbers_3_4 PASSED                                                                                                                                                                                             [ 50%]
test_um_pytest.py::test_strings_a_3 PASSED                                                                                                                                                                                             [100%]

========================================================================================================== 2 passed in 0.07 seconds ==========================================================================================================

```


#### pytest fixtures

Although unittest does allow us to have setup and teardown, pytest extends this quite a bit.
We can add specific code to run:

* at the beginning and end of a module of test code (setup_module/teardown_module)
* at the beginning and end of a class of test methods (setup_class/teardown_class)
* alternate style of the class level fixtures (setup/teardown)
* before and after a test function call (setup_function/teardown_function)
* before and after a test method call (setup_method/teardown_method)

Full example **test_um_pytest2.py**:

```
from unnecessary_math import multiply

def setup_module(module):
    print("setup_module      module:%s" % module.__name__)

def teardown_module(module):
    print("teardown_module   module:%s" % module.__name__)

def setup_function(function):
    print("setup_function    function:%s" % function.__name__)

def teardown_function(function):
    print("teardown_function function:%s" % function.__name__)

def test_numbers_3_4():
    print('test_numbers_3_4  <============================ actual test code')
    assert multiply(3,4) == 12

def test_strings_a_3():
    print('test_strings_a_3  <============================ actual test code')
    assert multiply('a',3) == 'aaa'


class TestUM:

    def setup(self):
        print("setup             class:TestStuff")

    def teardown(self):
        print("teardown          class:TestStuff")

    def setup_class(cls):
        print("setup_class       class:%s" % cls.__name__)

    def teardown_class(cls):
        print("teardown_class    class:%s" % cls.__name__)

    def setup_method(self, method):
        print("setup_method      method:%s" % method.__name__)

    def teardown_method(self, method):
        print("teardown_method   method:%s" % method.__name__)

    def test_numbers_5_6(self):
        print('test_numbers_5_6  <============================ actual test code')
        assert multiply(5,6) == 30

    def test_strings_b_2(self):
        print('test_strings_b_2  <============================ actual test code')
        assert multiply('b',2) == 'bb'
```

Expected result:

```
$ py.test -v test_um_pytest2.py
============================================================================================================ test session starts =============================================================================================================
platform darwin -- Python 3.7.0, pytest-3.8.0, py-1.6.0, pluggy-0.7.1 -- /Users/jasiplum/Development/Projects/Tieto/Python/naucse/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/jasiplum/Development/Projects/Tieto/Python/naucse, inifile:
collected 4 items

test_um_pytest2.py::test_numbers_3_4 PASSED                                                                                                                                                                                            [ 25%]
test_um_pytest2.py::test_strings_a_3 PASSED                                                                                                                                                                                            [ 50%]
test_um_pytest2.py::TestUM::test_numbers_5_6 PASSED                                                                                                                                                                                    [ 75%]
test_um_pytest2.py::TestUM::test_strings_b_2 PASSED                                                                                                                                                                                    [100%]

========================================================================================================== 4 passed in 0.08 seconds ==========================================================================================================
```

You can also run unittests and doctest with pytest.:w


### Other testing tools

#### Unit tests

pytest-cov: display the test coverage of your project

pytest-flake8: linter to make sure that your code is following the PEP8 style

Tox: http://tox.readthedocs.io - Tox can automate the creation of separate environments to run your tests.

#### Functional tests

WebTest: http://webtest.readthedocs.io

#### Load tests

Apache Bench

Boom: https://github.com/tarekziade/boom

Molotov: ttps://github.com/tarekziade/molotov

locust.io: http://docs.locust.io

#### End-to-end tests

Selenium: http://docs.seleniumhq.org/


### Developer documentation

Sphinx: http://www.sphinx-doc.org/

The following is a full example of a project documentation using Sphinx:

```
Myservice
=========
 
 
**myservice** is a simple JSON Flask application that uses **Flakon**.
 
The application is created with :func:`flakon.create_app`: 
.. literalinclude:: ../../myservice/app.py
 
 
The :file:`settings.ini` file which is passed to :func:`create_app`
contains options for running the Flask app, like the DEBUG flag: 
.. literalinclude:: ../../myservice/settings.ini
   :language: ini
 
 
Blueprint are imported from :mod:`myservice.views` and one 
Blueprint and view example was provided in :file:`myservice/views/home.py`: 
 
.. literalinclude:: ../../myservice/views/home.py 
   :name: home.py 
   :emphasize-lines: 13 
 
 
Views can return simple mappings (as highlighted in the example above), 
in that case, they will be converted into a JSON response. 
```

{{ figure(
     img=static('sphinx.png'),
     alt='Sphinx',)
}}
