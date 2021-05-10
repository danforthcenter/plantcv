# Warnings handling

import sys

def warn(warning):
    """Print out warning message

    Inputs:
    warning_msg = warning message text

    :param warning: str
    """
    warning_msg = f"Warning: {warning}"
    print(warning_msg, file=sys.stderr)
