# Warnings handling

import sys

def deprecation_warning(warning):
    """Print out warning message

    Inputs:
    warning = warning message text

    :param warning: str
    """
    print(warning, file=sys.stderr)
