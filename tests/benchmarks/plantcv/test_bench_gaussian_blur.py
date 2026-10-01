from plantcv import plantcv as pcv


def test_bench_gaussian_blur(benchmark, sized_rgb):
    """Blur cost should grow roughly linearly with pixel count."""
    benchmark.extra_info["pixels"] = sized_rgb.shape[0] * sized_rgb.shape[1]
    benchmark(pcv.gaussian_blur, img=sized_rgb, ksize=(51, 51))
