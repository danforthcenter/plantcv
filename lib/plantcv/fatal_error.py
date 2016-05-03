# Error handling


def fatal_error(error):
    """Print out the error message that gets passed, then quit the program.

    Inputs:
    error = error message text

    :param error: str
    :return:
    """

    raise RuntimeError(error)
