# Default Python packages.
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_arguments(arguments: list[list]) -> dict:
    """
    Parse extra arguments given in the command line.

    Parameters
    ----------
    arguments: list[list]
        The flags, description and required boolean per argument in a list.

    Returns
    -------
    dict:
        Extra arguments as a dictionary.
    """
    # Get information per argument and assert lists are equal in length.
    flags = [arg[0] for arg in arguments]
    descriptions = [arg[1] for arg in arguments]
    required = [arg[2] for arg in arguments]

    # Argument parser for the Python script.
    parser = ArgumentParser(description='extra command line arguments',
                            formatter_class=ArgumentDefaultsHelpFormatter)

    # Add the arguments to the parser.
    for i in range(len(arguments)):
        parser.add_argument(*flags[i], help=descriptions[i], required=required[i])

    # Create a dictionary containing all the arguments.
    args = parser.parse_args()
    return vars(args)
