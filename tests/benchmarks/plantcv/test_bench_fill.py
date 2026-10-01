from plantcv import plantcv as pcv


def test_bench_fill(benchmark, labeled_blobs):
    _, binary, n = labeled_blobs
    benchmark.extra_info["n_objects"] = n
    benchmark(pcv.fill, bin_img=binary, size=50)
