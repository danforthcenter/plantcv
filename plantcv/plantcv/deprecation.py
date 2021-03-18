# Deprecation handling

import warnings
from plantcv.plantcv import _version
def deprecation_warning(warning):
    """Print out deprecation warning

    :param warning: warning message text
    :return:
    """
    version = _version.get_versions()
    warning_msg = "{} \nCurrent PlantCV version: {} released on {}".format(warning, version["version"], version['date'])
    warnings.warn(warning_msg, DeprecationWarning, stacklevel=2)
