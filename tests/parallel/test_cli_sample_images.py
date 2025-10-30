import os
import pytest
from plantcv.parallel.cli_sample_images import main


def test_run_sample_images(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-sample",
                "--source", parallel_test_data.snapshot_imgdir,
                "--outdir", os.path.join(str(tmp_dir), "sample_images"),
                "--number", "3"]
    assert main() is None
