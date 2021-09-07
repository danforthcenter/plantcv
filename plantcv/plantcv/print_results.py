# Print Numerical Data

from plantcv.plantcv import outputs


def print_results(filename):
    """Print result table

    Inputs:
    filename = filename

    :param filename: str
    :return:
    """
    print("""Deprecation warning: plantcv.print_results will be removed in a future version.
             Please use plantcv.outputs.save_results instead.
          """)
    outputs.save_results(filename=filename, outformat="json")
