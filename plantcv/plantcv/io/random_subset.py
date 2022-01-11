# Random Subset a list

import random
from plantcv.plantcv import fatal_error


def random_subset(dataset, num=100, seed=None):
    """
    Get a random subset of the elements in a list.
    Inputs:
    dataset      = List to be subset
    num          = Number of elements in the resulting subset
    seed         = Optional seed for the random number generator
    Returns:
    sub_dataset = List of 'num' elements randomly drawn from 'dataset'
    :param dataset: list
    :param num: int
    :param seed: int
    :return sub_dataset: list
    """
    random.seed(a=seed)

    # Check to make sure number of imgs to select is less than number of images found
    N = len(dataset)
    if num > N:
        fatal_error("Number of images found less than 'num'.")

    # Get random images
    samples = random.sample(dataset, k=num)

    return samples
