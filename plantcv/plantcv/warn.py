# Warnings handling

import sys


def warn(warning):
    """Print out warning message

    Inputs:
    warning = warning message text

    :param warning: str
    """
    print(f"Warning: {warning}", file=sys.stderr)
