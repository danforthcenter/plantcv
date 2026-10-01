import numpy as np
from plantcv import plantcv as pcv


def test_bench_analyze_size(benchmark, labeled_blobs):
    """analyze.size loops over labels; watch for superlinear growth in n."""
    labeled, binary, n = labeled_blobs
    img = np.dstack([binary] * 3)
    benchmark.extra_info["n_objects"] = n
    # pedantic mode: fewer rounds, because the 1000-object case is slow
    # and Outputs has to be cleared between rounds
    benchmark.pedantic(pcv.analyze.size,
                       kwargs={"img": img, "labeled_mask": labeled, "n_labels": n},
                       setup=pcv.outputs.clear, rounds=5, iterations=1)
