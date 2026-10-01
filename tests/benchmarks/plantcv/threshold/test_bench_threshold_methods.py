from plantcv import plantcv as pcv


def test_bench_threshold_binary(benchmark, sized_rgb):
    """Benchmark for PlantCV"""
    gray_img=pcv.rgb2gray(sized_rgb)
    benchmark(pcv.threshold.binary, gray_img=gray_img, threshold=125)


def test_bench_threshold_gaussian(benchmark, sized_rgb):
    """Benchmark for PlantCV"""
    gray_img=pcv.rgb2gray(sized_rgb)
    benchmark(pcv.threshold.gaussian, gray_img=gray_img, ksize=5, offset=5)
