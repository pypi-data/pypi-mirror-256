# Default Python packages.
from sys import exit as sys_exit
from time import time
from traceback import format_exc
from typing import Callable, Union


class TestSuite:
    """
    Parent class to define and run test cases with.
    """
    def __init__(self):
        self.results = {}

    def _get_test_cases(self) -> list:
        """
        Get all test cases defined in the child class.

        Returns
        -------
        list:
            All the test cases defined in the child class.
            Returns an empty list when the parent class is used directly.
        """
        # Get all child class attributes.
        child = self
        child_all = dir(self)
        child_attributes = list(self.__dict__.keys())

        # Get all parent class methods.
        parent = self.__class__.__base__
        parent_methods = dir(parent)

        # Get child methods which are not in parent class.
        tests = [test for test in child_all if test not in parent_methods]
        tests = [test for test in tests if test not in child_attributes]

        # Return empty list when parent class is used directly.
        if self.__class__.__base__ == object:
            tests = []

        return [getattr(child, test) for test in tests]

    def _run_test_suite_method(self, method: Callable) -> bool:
        """
        Run a test suite method.

        Parameters
        ----------
        method: Callable
            The test suite method to be run.

        Returns
        -------
        bool:
            True: the test suite method succeeded.
            False: the test suite method failed.
        """
        name = method.__name__
        success = False
        message = None
        trace = None

        try:
            method()
            success = True
        except Exception as error:
            message = f"{error.__class__.__name__}: {error}"
            trace = format_exc()

        if not success:
            print(f"{name} FAILED:\n{trace}")

        self.results[name] = {"success": success, "message": message, "traceback": trace}
        return success

    def _run_test_case(self, test_case: Callable) -> bool:
        """
        Run a test case method including its setup and teardown.

        Parameters
        ----------
        test_case: Callable
            The test case method to be run.

        Returns
        -------
        bool:
            True: the test case, including its setup and teardown, succeeded.
            False: either the test case, its setup, or its teardown failed.
        """
        name_case = test_case.__name__
        name_setup = self.set_up_test_case.__name__
        name_teardown = self.tear_down_test_case.__name__

        # Return False when test case setup fails.
        if not self._run_test_suite_method(method=self.set_up_test_case):
            # Replace test case setup key with test case method key in results.
            self.results[name_case] = self.results.pop(name_setup)
            return False

        # Run test case.
        success = self._run_test_suite_method(method=test_case)

        # Return False when test case teardown fails.
        if not self._run_test_suite_method(method=self.tear_down_test_case):
            # Replace test case setup key with test case method key in results.
            self.results[name_case] = self.results.pop(name_teardown)
            return False

        return success

    def run_test_suite(self, do_exit: bool = True, do_summary: bool = True) -> Union[bool, int]:
        """
        Run the entire test suite including its setups and teardowns.

        Parameters
        ----------
        do_exit: bool
            Exit the interpreter once the test suite has run.
        do_summary: bool
            Print a summary of the test suite run in the console.

        Returns
        -------
        bool:
            True: all test suite methods succeeded.
            False: some test suite methods failed.
        int:
            0: all test suite methods succeeded.
            1: some test suite methods failed.
        """
        start = time()

        # Reset results.
        self.results = {}

        # Run test suite setup and exit/return if it fails.
        if not self._run_test_suite_method(method=self.set_up_test_suite):
            return sys_exit(1) if do_exit else False

        # Run all test cases.
        success = {"bool": True, "code": 0}
        tests = self._get_test_cases()

        for test in tests:
            if not self._run_test_case(test_case=test):
                success = {"bool": False, "code": 1}

        # Run test suite teardown.
        if not self._run_test_suite_method(method=self.tear_down_test_suite):
            success = {"bool": False, "code": 1}

        end = time()

        # Print test suite summary.
        if do_summary:
            length = len(tests)
            duration = round(end - start, 3)
            message = f"Ran {length} test cases in {duration} seconds.\n\n"

            if not success["bool"]:
                for result in self.results.keys():
                    if not self.results[result]["success"]:
                        message += f"{result}: {self.results[result]['message']}\n"
            else:
                message += "All tests passed!\n"

            front = f"Test summary '{self.__class__.__name__}'"
            back = f"{len(front) * '-'}"
            front = f"{front}\n{len(front) * '-'}\n"

            print(f"\n{front}{message}{back}\n")

        # Return/exit success of test suite run.
        return sys_exit(success["code"]) if do_exit else success["bool"]

    def set_up_test_suite(self):
        """
        Editable placeholder for the test suite setup.
        """

    def tear_down_test_suite(self):
        """
        Editable placeholder for the test suite teardown.
        """

    def set_up_test_case(self):
        """
        Editable placeholder for the test case setup.
        """

    def tear_down_test_case(self):
        """
        Editable placeholder for the test case setup.
        """
