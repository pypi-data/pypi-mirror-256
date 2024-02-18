# Default Python packages.
from multiprocessing import Process, Queue, cpu_count, current_process, Lock
from multiprocessing.synchronize import Lock as LockType
from threading import Thread
from typing import Callable, Optional, List, Union


def _create_queue(parameters: list[list]) -> Queue:
    """
    Transform a list with sets of parameters into a FIFO queue.

    Parameters
    ----------
    parameters: list[list]
        Sets of parameters in a list to create the queue with.

    Returns
    -------
    Queue:
        Given parameters in a FIFO queue.
    """
    queue = Queue()

    for parameter in parameters:
        queue.put(parameter)

    return queue


def _run_multi(multi: str, target: Callable, parameters: list[list],
               number: Optional[int] = None, lock: bool = False) -> None:
    """
    Shared steps in the 'run_processes' and 'run_threads' functions.

    Parameters
    ----------
    multi: str:
        Either "processes" or "threads".
    target: Callable
        Any callable object to be run repeatedly.
    parameters: list[list]
        Sets of parameters in a list to repeatedly run the callable with.
    number: Optional[int]
        Number of subprocesses or threads to run.
    lock: bool
        Use a lock to ensure a resource is only accessed once at any given time.
    """
    # Create a FIFO queue containing the given parameters.
    queue = _create_queue(parameters=parameters)

    # Define arguments for the processes / threads.
    args = [target, queue, Lock()] if lock else [target, queue]
    subs: List[Union[Process, Thread]] = []

    # Create processes equal to given number, or equal to available CPU cores.
    if multi == "processes":
        number = cpu_count() if number is None else number

        for _ in range(number):
            subs.append(Process(target=_run_target, args=args))

    # Create threads equal to given number, or equal to 8x available CPU cores.
    elif multi == "threads":
        number = cpu_count() * 8 if number is None else number

        for _ in range(number):
            subs.append(Thread(target=_run_target, args=args))

    # Start the subprocesses / threads and wait for them to finish before continuing.
    for _ in subs:
        _.start()
    for _ in subs:
        _.join()

    # Raise error in main process if error was raised in a subprocess.
    if multi == "processes":
        if any([_.exitcode for _ in subs]):
            raise ChildProcessError()

    # Close the queue and its thread.
    queue.close()
    queue.join_thread()


def _run_target(target: Callable, parameters: Queue, lock: Optional[LockType] = None) -> None:
    """
    Repeatedly run a callable until its queue is empty.

    Parameters
    ----------
    target: Callable
        Any callable object to be run repeatedly.
    parameters: Queue
        Sets of parameters in a queue to repeatedly run the callable with.
    lock: Optional[LockType]
        Append the lock to the set of parameters.
    """
    while not parameters.empty():
        parameter = parameters.get()
        target(*parameter, lock) if lock is not None else target(*parameter)


def run_processes(target: Callable, parameters: list[list], processes: Optional[int] = None,
                  lock: bool = False) -> None:
    """
    Run computationally heavy workloads faster by using multiprocessing.
    See the readme for an example.

    Parameters
    ----------
    target: Callable
        Any callable object to be run repeatedly.
    parameters: list[list]
        Sets of parameters in a list to repeatedly run the callable with.
    processes: Optional[int]
        Number of subprocesses to run.
        It can be equal to or less than the number of available CPU cores.
        It is the number of available CPU cores by default.
    lock: bool
        Use a lock to ensure a resource is only accessed once at any given time.
    """
    if current_process().name != "MainProcess":
        raise ChildProcessError("endless recursion detected")

    _run_multi(multi="processes", target=target, parameters=parameters,
               number=processes, lock=lock)


def run_threads(target: Callable, parameters: list[list], threads: Optional[int] = None,
                lock: bool = False) -> None:
    """
    Run I/O heavy workloads faster by using multithreading.
    See the readme for an example.

    Parameters
    ----------
    target: Callable
        Any callable object to be run repeatedly.
    parameters: list[list]
        Sets of parameters in a list to repeatedly run the callable with.
    threads: Optional[int]
        Number of threads to run.
        It is eight times the number of available CPU cores by default.
    lock: bool
        Use a lock to ensure a resource is only accessed once at any given time.
    """
    _run_multi(multi="threads", target=target, parameters=parameters,
               number=threads, lock=lock)
