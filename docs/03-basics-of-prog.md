# intro-to-python

## Basics of Programming With Python
This section introduces the basic concepts involved in computer programming or software engineering as it is also known.

_The syntax presented below is that of Python but other languages have the same concepts and work similarly._

Please note this is not an exhaustive list of concepts.

See the Python docs for more at [https://docs.python.org/](https://docs.python.org/)


### Variables / Constants
A variable is just a shorthand way of referencing a place in memory that has a particular type - like a number or a string.

In Python you define a variable by just assigning a value to it.

```python
num = 1
dec_num = 1.75

my_message = 'My Message'
```

Variables in Python are written in "snake case"; that is all lower case where each word is separated with an underscore character - '_'.

A constant is like a variable but it denotes a value that should not change. It is named in all upper case.

```python
MY_CONST_WINDOW_WIDTH = 800

# Names can contain numbers after the first letter
PI_6 = 3.141593
PI_10 = 3.1415926536

SPACE_CHAR = ' '
```
_See [03_vars_/game.py](../examples/03_vars/vars.py)_

### Functions
A function in Python is declared using the def keyword and is called by adding parentheses () to its name.

```python
def add_2_numbers(n1, n2):
    return n1 + n2

result = add_2_numbers(1, 2)
print(result)  # prints 3
```

### Lists
Lists in Python are denoted by square brackets [] and are indexed starting at 0.

```python
my_list = [1, 2, 3]

print(my_list[0])  # prints 1
print(my_list[1])  # prints 2

# a for loop iterates over the list one element at a time:
for elem in my_list:
    print(elem)

# prints:
1
2
3
```

### Args / Kwargs
When passing arguments (or args) to functions, Python allows for 3 different types.
- positional parameters - these are passed so they line up with their associated placeholders.
From our example above - `add_2_numbers(1, 2)` - 1 is passed as n1 and 2 as n2.
- args list - all non-positional args (that are not keyword args) are collected into a list called args by convention.
```python
def add_2_numbers(n1, n2, *args):
    # args would contain ['some', 'more', 'args'] here
    return n1 + n2

result = add_2_numbers(1, 2, 'some', 'more', 'args')
print(result)  # prints 3
```
- keyword args (or kwargs) - represents a dictionary of keyword / value pairs for other things not explicitly specified in the function's parameter list.
```python
def add_2_numbers(n1, n2, **kwargs):
    # kwargs would contain { verbose=True, color='red' } here
    return n1 + n2

result = add_2_numbers(1, 2, verbose=True, color='red')
print(result)  # prints 3
```

### Modules / Imports
A module in Python is basically a `.py` file.

By default, only certain things like [Built-in Functions](https://docs.python.org/3/library/functions.html) are automatically made available to a Python program. This is to minimize the amount of RAM a simple Python script needs to execute.

To bring additional features into scope for a Python module, the import statement is used. These might be for optional features in the Python [_standard library_](https://docs.python.org/3/library/index.html) or stdlib, or 3rd party libraries like pygame.

After the import statement those things are available for use in that module only. Every module needs to `import` the features it needs.

```python
from random import randint

import pygame

from my_custom_module import MyClass, my_function  # from my_custom_module.py

```

### Objects
Almost everything in Python is an object. Things like numbers, strings, modules are all objects.

A custom object variable (or constant) can be created like this.
```python
my_object = {
    'verbose': True,
    'color': 'red',
    'add2': add_2_numbers
}

print(my_object['verbose'])  # prints True
print(my_object['color'])  # prints red
print(my_object['add2'](1, 2))  # prints 3

# You can think of this last line as 2 separate statements.
# That might make it more clear what is happening.

add2 = my_object['add2']  # The value assigned to add2 is a reference to the function add_2_numbers

print(add2(1, 2))  # prints 3
```

### Classes
A class is a blueprint for creating object instances. They are named in TitleCase and are called like a function.

Each _method_ - a function declaration within the class - receives a first arg of _self_. `self` is a reference to the object instance and allows you to access instance properties like `self.first_name` and `self.last_name` below.

For example:
```python
class Person:
    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last
    
    def full_name(self):
        # values for the object instance referenced by self
        return f`{self.first_name} {self.last_name}`

person1 = Person('John', 'Doe')
print(person1.full_name())  # prints John Doe

person2 = Person('Charlie', 'Brown')
print(person2.full_name())  # prints Charlie Brown

```

### Using a custom module for configuration
As the number of constants grow in your app it can be helpful to create a custom module to hold all the configuration data. This makes sure that all configuration data is in one place to make it easier to maintain / modify when needed.

_See [03_config/game.py](../examples/03_config/game.py) and [03_config/config.py](../examples/03_config/config.py)_

```python
# config.py
settings = {
    'screen': {
        'width': 1024,
        'height': 768,
        'bg_color': 'purple'
    },
    'title': 'My awesome game'
}

# game.py
import pygame

from config import settings


# pygame setup
pygame.init()
pygame.display.set_caption(settings['title'])

# Variables
screen = pygame.display.set_mode((settings['screen']['width'], settings['screen']['height']))

```

## See Also
- [https://docs.python.org/](https://docs.python.org/)
- [Tutorial](https://docs.python.org/3/tutorial/index.html)
- [Python HOWTOs](https://docs.python.org/3/howto/index.html)
