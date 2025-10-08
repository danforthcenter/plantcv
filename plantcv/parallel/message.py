import sys


def parallel_print(message, file=sys.stdout, verbose=True):
    if verbose:
        print(message, file=file)
