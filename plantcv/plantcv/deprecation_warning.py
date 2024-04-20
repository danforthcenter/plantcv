# Deprecation handling

import sys
from plantcv.plantcv import __version__ as version
from plantcv.plantcv import params


def deprecation_warning(warning):
    """Print out deprecation warning

    Inputs:
    warning = warning message text

    :param warning: str
    """
    warning_msg = f"DeprecationWarning: {warning} Current PlantCV version: {version}"
    if params.verbose is True:
        print(warning_msg, file=sys.stderr)
