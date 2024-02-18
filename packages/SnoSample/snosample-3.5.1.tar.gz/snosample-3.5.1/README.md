# SnoSample

Simplified tools for Python projects.

## Installation

To install the SnoSample package run the following command:

```shell
pip install snosample
```

Alternatively, install the package via your IDE.

## Usage

This section provides simple code examples to understand the package fundamentals.
For more details about specific parameters, consult the respective docstring.

#### Testing

A simple and easy to use test suite:

```python
from snosample.testing import TestSuite


class MyTestSuite(TestSuite):
   
   def __init__(self):
      super().__init__()
       
      # Add extra attributes to your test case.
      self.extra = True
      
   def set_up_test_suite(self):
      # This optional method will be called before running the test suite.
      return
   
   def tear_down_test_suite(self):
      # This optional method will be called after running the test suite.
      return
   
   def set_up_test_case(self):
      # This optional method will be called before each test case.
      return
   
   def tear_down_test_case(self):
      # This optional method will be called after each test case.
      return
   
   def test_function_1(self):
      # Successful test case.
      return
   
   def test_function_2(self):
      # Failing test case.
      raise ValueError("something went wrong")

if __name__ == "__main__":
    # Run test suite, print failing test cases, optionally a summary, and exit.
    tests = MyTestSuite()
    tests.run_test_suite(do_summary=True, do_exit=True)
```

#### Logging

A simple and easy to use logger:

```python
from snosample.logging import Logger

# The default logger only prints to the console with an "info" threshold.
logger = Logger()
logger.message(message="hello!", level="warning")

# But these parameters can be changed.
logger = Logger(console=False, console_level="info",
                file="path/to/logfile", file_level="debug",
                layout="<level> | <message> | <time>")
logger.message(message="hello!", level="info")
```

#### Arguments

Add extra arguments to your Python script:

```shell
python "example.py" --arg1 "required" --arg2 "optional"
```

The command below will give an error and print the description for arg1:

```shell
python "example.py" --arg2 "optional"
```

The "-h" and "--help" flags can be used to view these arguments from the command line:

```shell
python "example.py" --help
```

The "example.py" script used in the command line:

```python
from snosample import parse_arguments

if __name__ == "__main__":
    # Define a required argument with flags and a description.
    req_flags = ["--arg1", "-r"]
    req_help = "a required argument"
    req_req = True
    req = [req_flags, req_help, req_req]
   
    # Define an optional argument with flags and a description.
    opt_flags = ["--arg2", "-o"]
    opt_help = "an optional argument"
    opt_req = False
    opt = [opt_flags, opt_help, opt_req]

    args = [req, opt]

    # Get the dictionary with the given values from the command line.
    args = parse_arguments(arguments=args)

    # Rest of code using the arguments.
    print(args["arg1"])
```

#### Assertions

Make assertions either within or outside test suites:

```python
from snosample.assertions import *

assert_equal(calc, true)
assert_not_equal(calc, true)

assert_true(expression)
assert_false(expression)

# Assert if two variables are almost equal within the given margin.
assert_almost_equal(calc, true, margin, relative=True)  # use fraction of true.
assert_almost_equal(calc, true, margin, relative=False)  # use margin directly.

# Assert if callable raises expected exception with the given args and/or kwargs.
assert_raises(action, expected, args, kwargs)
```

#### Multiprocessing

Run computationally heavy functions parallel with subprocesses:

```python
from snosample.multi import run_processes

# Only used to show which process did the 'calculation'.
from time import sleep
from multiprocessing import current_process

def heavy_function(calculate: int):
    # 'heavy' calculation.
    sleep(calculate)
    
    process = current_process().name
    print(f"{process} | I performed calculations for {calculate} seconds.")


print("All code outside if name is main statement is executed repeatedly!")

if __name__ == "__main__":
   print("This will be printed only once.")
   
   # Create parameters to call the heavy function with.
   parameters = []
   
   for i in range(16):
      parameters.append([i])
   
   # Run the heavy function with subprocesses.
   run_processes(target=heavy_function, parameters=parameters)
```

#### Multithreading

Run I/O heavy functions parallel with threads and a lock:

```python
from snosample.multi import run_threads, LockType

# Only used to show which thread is writing in the file.
from threading import current_thread


# Always make the lock the last parameter in the function.
def heavy_function(file: str, nap: int, lock: LockType):
    # Ensure no other threads are using the file resource at the same time.
    lock.acquire()
    
    # I/O operation.
    with open(file, "a") as file:
        thread = current_thread().name
        file.writelines(f"{thread} | I slept for {nap} seconds.\n")

    # Release the lock so other threads can write to the file as well.
    lock.release()


if __name__ == "__main__":
   # Create parameters to call the heavy function with.
   parameters = []
   
   for i in range(128):
      parameters.append(["./example.txt", i])
   
   # Run the heavy I/O function with threads, the lock is added automatically.
   run_threads(target=heavy_function, parameters=parameters, lock=True)
```

## Features

#### SnoSample module

1. The user is able to define extra arguments for the Python script,  
   when running it from the command line:
   1. these arguments can be required.
   2. these arguments can be optional.
   3. an error is raised when the required arguments are not given.
   4. an error is raised when an unknown argument is given.
   5. these arguments can be viewed from the command line.

#### SnoSample.testing module

1. The user is able to define test cases inside a test suite.
2. The user is able to run all test cases with a single command:
   1. this command shows if the test suite succeeded.
   2. this command can exit with code 1 when the test suite fails.
3. The user is able to see the test case results after each run:
   1. these results show if a test case failed.
   2. these results show why a test case failed.
   3. these results reset before each run.
   4. these results include the traceback if an error is raised.
4. The user is able to define a test suite setup:
   1. this setup is optional.
   2. this setup can be run independently of the test cases.
   3. this setup triggers automatically when the test suite is run.
   4. the test cases will not be run when this setup fails.
5. The user is able to define a test suite teardown:
   1. this teardown is optional.
   2. this teardown can be run independently of the test cases.
   3. this teardown triggers automatically when the test suite is run.
6. The user is able to define a test case setup:
   1. this setup is optional.
   2. this setup can be run independently of the test cases.
   3. this setup triggers automatically before each test case.
   4. this setup shows its results under the respective test case when not successful.
7. The user is able to define a test case teardown:
   1. this teardown is optional.
   2. this teardown can be run independently of the test cases.
   3. this teardown triggers automatically after each test case. 
   4. this teardown shows its results under the respective test case when not successful.
8. The user is able to assert if two variables are (un)equal:
   1. these variables can be booleans.
   2. these variables can be strings.
   3. these variables can be integers or floats.
   4. these variables can be lists or tuples.
   5. these variables can be dictionaries.
   6. these variables can be numpy arrays.
9. The user is able to assert if two variables are almost equal within a margin:
   1. the user can define this margin.
   2. this margin can be relative or absolute.
   3. these variables can be integers or floats.
   4. these variables can be lists or tuples with integers and/or floats.
   5. an error is raised when these variables have different/no sizes.
   6. an error is raised when these variables contain a non-numeric value.
   7. these variables can be numpy arrays.
10. The user is able to assert if an expression is True.
11. The user is able to assert if an expression is False.
12. The user is able to assert if executing a callable raises an error:
    1. the user can define the callable including its arguments.
    2. the user can define the expected type of error raised.
    3. an error is raised when the error is not as expected.
    4. an error is raised when no error is raised.
13. A test suite summary is printed to the console when running the test cases:
    1. this summary includes the result of the test suite setup.
    2. this summary includes the result of each test case.
    3. this summary includes the result of the test suite teardown.
    4. this summary can be optional.

#### SnoSample.logging module

1. The logger is able to show messages in the console:
   1. the user can define these messages.
2. The logger is able to write messages to a text file:
   1. the user can define these messages.
   2. the user can define this file path.
   3. the logger raises an error when the file path does not exist.
   4. this text file does not need to exist.
   5. this text file is overwritten by the messages.
3. The logger is able to show the time at which the message was generated.
4. The logger is able to show the level of the message:
   1. the user can define this level.
   2. the accepted message levels are: 'debug', 'info', 'warning', 'error'.
   3. an error is raised when an unacceptable message level is given.
   4. debug messages have a blue colour in the console.
   5. info messages have a white colour in the console.
   6. warning messages have a yellow colour in the console.
   7. error messages have a red colour in the console.
5. The user is able to define a message level threshold:
   1. the accepted thresholds are: 'debug', 'info', 'warning', 'error'.
   2. an error is raised when an unacceptable message level is given.
   3. all messages below this threshold will not be shown by the logger.
   4. this threshold can be different for the file and the console messages.
6. The user is able to define a layout for the messages:
   1. an error is raised when the message is not included in the layout.
   2. this layout can include extra substrings defined by the user.

#### SnoSample.multi module

1. The user is able to spawn subprocesses targeting a callable:
   1. this callable can be defined by the user.
   2. the list of parameter sets or this callable can be defined by the user.
   3. the number of these subprocesses can be defined by the user.
   4. these subprocesses terminate automatically when the callable has run.
   5. the callable is only run once per parameter set.
   6. the main process waits for these subprocesses to finish before continuing.
   7. a lock can be defined by the user.

2. The user is able to spawn threads targeting a callable:
   1. this callable can be defined by the user.
   2. the list of parameter sets or this callable can be defined by the user.
   3. the number of these threads can be defined by the user.
   4. these threads terminate automatically when the callable has run.
   5. the callable is only run once per parameter set.
   6. the main process waits for these threads to finish before continuing.
   7. a lock can be defined by the user.

## Changelog

#### v3.5.1

- Project is open source.

#### v3.5.0

- Revision of project structure.
- Revision of documentation.

#### v3.4.6

- SnoSample.testing feature 9 bugfix.
- Revision of documentation.

#### v3.4.5

- SnoSample.logging features 4.4 through 4.7 added.
- SnoSample.multi features 1.7 and 2.7 added.
- Revision of project structure.

#### v3.4.4

- SnoSample.testing feature 9 bugfix.

#### v3.4.3

- SnoSample.testing feature 13 bugfix.

#### v3.4.2

- SnoSample.testing feature 3.4 added.
- SnoSample.testing feature 13 bugfix.

#### v3.4.1

- SnoSample.testing feature 9 bugfix.

#### v3.4.0

- SnoSample.testing features 8.6 and 9.7 added.

#### v3.3.0

- SnoSample.testing features 2.2 and 13 added.

#### v3.2.0

- SnoSample.testing features 8 through 12 added.

#### v3.1.3

- SnoSample.multi features 1 and 2 added.

#### v2.1.3

- Revision of licence.

#### v2.1.2

- SnoSample feature 1 added.

#### v2.0.2

- Revision of project structure.

#### v2.0.1

- Revision of documentation.

#### v2.0.0

- SnoSample.logging features 1 through 6 added.

#### v1.0.0

- SnoSample.testing features 1 through 7 added.

#### v0.1.0

- Initial release.
