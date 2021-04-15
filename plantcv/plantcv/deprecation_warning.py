# Deprecation handling

import sys
from plantcv.plantcv import _version
from plantcv.plantcv import params

def deprecation_warning(warning):
    """Print out deprecation warning

    Inputs:
    warning = warning message text

    :param warning: str
    """
    version = _version.get_versions()
    warning_msg = f"DeprecationWarning: {warning} Current PlantCV version: {version['version']} released on {version['date']}"
    if params.verbose is True:
        print(warning_msg, file=sys.stderr)
