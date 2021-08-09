import random
from plantcv.plantcv import fatal_error


def random_subset(dataset, num=100, seed=None):
    
    random.seed(a=seed)

    # Check to make sure number of imgs to select is less than number of images found
    N = len(dataset)
    if num > N:
        fatal_error("Number of images found less than 'num'.")

    # samples = []
    # indices = []

    # Get random images
    samples = random.sample(dataset, k=num)
    # for i in range(0, num):
    #     idx = random.randint(0, N - 1)
    #     while idx in indices:
    #         idx = random.randint(0, N - 1)
    #     samples.append(dataset[idx])
    #     indices.append(idx)

    return samples
