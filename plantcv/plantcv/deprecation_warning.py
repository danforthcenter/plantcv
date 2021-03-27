# Deprecation handling

import warnings
from plantcv.plantcv import _version
# from plantcv.plantcv import __version__


def deprecation_warning(warning):
    """Print out deprecation warning

    Inputs:
    warning = warning message text

    :param warning: str
    """
    version = _version.get_versions()
    # f string
    # warning_msg = "{} \nCurrent PlantCV version: {} released on {}".format(warning, version["version"],
    # version['date'])
    warning_msg = f"{warning} Current PlantCV version: {version['version']} released on {version['date']}"
    warnings.warn(warning_msg, DeprecationWarning, stacklevel=2)
