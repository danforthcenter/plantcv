# Print Numerical Data


def print_results(filename, header, data):
    """Print result table

    Inputs:
    filename = filename
    header   = result data table headers
    data     = result data table values

    :param filename: str
    :param header: list
    :param data: list
    :return:
    """
    print('\t'.join(map(str, header)))
    print('\t'.join(map(str, data)))
