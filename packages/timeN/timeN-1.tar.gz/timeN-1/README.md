# Package Description

timeN is a simple package that contains a customizable `@timen` decorator which times how long it takes (in milliseconds) for the decorated function to run n times

# Usage

The timen decorator is quite simple to use. it can be imported by simply importing the timeN package with 
```python
import timeN
```
From there, the timeN decorator can be used like any other decorator, with the exception that you must end the decorator in parentheses since it takes optional parameters
```python
@timeN()
def foo():
    print("Hello World")
```
Output:
```
Hello World
...
Hello World
foo took 2.0 milliseconds to run 10 times
```
The 2 optional parameters are: n (number of times to run the function) and round_to (number decimal places to round the final result to).
```python
@timeN(100, 5)
def foo():
    print("Hello World")
```
Output:
```
Hello World
...
Hello World
foo took 11.99365 milliseconds to run 100 times
```